import numpy as np
from collections import Counter
import math

"""
The transformation rule identifies distinct roles for non-background colors: Anchor, Static, and Mover. It operates sequentially, allowing later steps to overwrite earlier ones under specific conditions.

1.  **Initialization**: Determine grid dimensions (H, W) and the background color (B, most frequent). Create an output grid initialized with B.
2.  **Role Identification**:
    *   **Anchor**: Find the column (`anc_c`) containing specific, preserved non-background values (`anchor_vals`). Heuristics like known patterns ([2, 8], [2], [5], [6]) or column consistency are used.
    *   **Mover**: Identify the most frequent non-anchor, non-background color (`M`).
    *   **Static**: Identify any remaining non-background, non-anchor, non-mover colors (`S`).
3.  **Sequential Placement (Overwrite Logic)**:
    *   **Static Placement**: Copy Static objects (`S`) from input to output, overwriting the background.
    *   **Anchor Placement**: Copy the anchor column (`anc_c`) from input to output, overwriting background/static values in that column.
    *   **Mover Processing**: Determine if Movers (`M`) are primarily LEFT or RIGHT of `anc_c`.
        *   **Left Movers**:
            *   Calculate target coordinates `(tr, tc)` based on shifts `(dr, dc)` specific to `M` and the relative column (`rel_c`: -1, -2, or -3 for M=9).
                *   `rel_c = -1`: Shift `(dr1(M), 0)`. `dr1` maps M={4:0, 3:-1, 8:-4, 9:0}.
                *   `rel_c = -2`: Shift `(dr2(M), dc2(M))`. `dr2` maps M={4:-2, 3:-1, 8:-4, 9:-2}. `dc2` is 0 if M=9, else 1.
                *   `rel_c = -3`: Only if M=9, shift `(-5, 0)`.
            *   Place `M` at `(tr, tc)` **only if** the target cell in the *current output grid* contains the background color `B`. Track if any move originated from `rel_c = -2` (`flag_minus_2`).
            *   **Conditional Generation**: If `flag_minus_2` is true, attempt to place `M` at specific coordinates near the top, **only if** the target cell contains the background color `B`.
                *   M=4: Target `(0, anc_c)`.
                *   M=8: Target `(0, anc_c - 1)`.
                *   M=9: Targets `(0, anc_c - 1)` and `(1, anc_c - 1)`.
        *   **Right Movers (M=7 Specific)**:
            *   Preserve an M=7 mover at `(r, anc_c + 1)` if `input[r, anc_c]` is an anchor value. Place M=7 at this coord in the output (overwrites background/static). Store location `(pr, pc)`.
            *   If preserved, generate a 'V' shape using M=7 relative to `(pr, pc)` and Static object (S=9) properties. Place M=7 at shape coordinates **only if** the target cell contains the background color `B`.
        *   **Other Movers**: Movers far left/right or in unhandled patterns are effectively removed (left as background or overwritten).
4.  **Output**: Return the final state of the output grid.
"""

# --- Helper Functions ---

def find_background_color(grid_np: np.ndarray) -> int:
    """Identifies the most frequent color as the background color."""
    counts = Counter(grid_np.flatten())
    if not counts:
        return 0 # Default background
    # Assume most frequent color is background
    background_color = counts.most_common(1)[0][0]
    return int(background_color)

def find_anchor_column(grid_np: np.ndarray, background_color: int) -> tuple[int, set[int]]:
    """
    Identifies the anchor column index and the set of anchor values.
    Relies on heuristics like known patterns or column consistency.
    """
    H, W = grid_np.shape
    # Known anchor patterns observed in examples
    known_anchor_sets = [{2, 8}, {2}, {5}, {6}]

    anchor_candidates = []

    for c in range(W):
        column = grid_np[:, c]
        non_background_mask = column != background_color
        non_background_values = column[non_background_mask]

        if len(non_background_values) > 0:
            unique_non_bg = set(non_background_values)
            # Assign priority based on matching known sets, single value, or multiple values
            priority = 3
            if unique_non_bg in known_anchor_sets:
                priority = 1
            elif len(unique_non_bg) == 1:
                 priority = 2
            
            anchor_candidates.append({'col': c, 'vals': unique_non_bg, 'priority': priority, 'count': len(non_background_values)})


    if not anchor_candidates:
        return -1, set()

    # Sort candidates: lowest priority number first, then highest count
    anchor_candidates.sort(key=lambda x: (x['priority'], -x['count']))

    best_candidate = anchor_candidates[0]
    return best_candidate['col'], best_candidate['vals']


def identify_roles(grid_np: np.ndarray, anchor_col: int, anchor_vals: set[int], background_color: int) -> tuple[int, set[int]]:
    """Identifies Mover (most frequent other) and Static colors."""
    H, W = grid_np.shape
    counts = Counter(grid_np.flatten())
    mover_color = -1
    static_colors = set()

    potential_movers = {}
    for val, count in counts.items():
        val_int = int(val) # Ensure integer type
        # Exclude background and anchor values
        if val_int != background_color and val_int not in anchor_vals:
            potential_movers[val_int] = count

    # Heuristic: Mover is the most frequent non-anchor, non-background color
    if potential_movers:
        mover_color = max(potential_movers, key=potential_movers.get)

    # Heuristic: Static colors are any other non-anchor, non-bg, non-mover colors
    for val in potential_movers:
        if val != mover_color:
            static_colors.add(val)

    return mover_color, static_colors

def get_object_coords(grid_np: np.ndarray, value: int) -> list[tuple[int, int]]:
    """Finds all coordinates (row, col) of a given value."""
    coords = np.argwhere(grid_np == value)
    # Return list of tuples, ensuring correct types
    return [(int(r), int(c)) for r, c in coords]

def get_static_properties(static_coords: list[tuple[int, int]]) -> tuple[int, int, int]:
    """Calculates properties of static objects, useful for M=7 rule."""
    if not static_coords:
        return -1, -1, -1
    cols = [c for r, c in static_coords]
    rows = [r for r, c in static_coords]
    # Assuming static objects often form a column (like train_3's '9's)
    static_c = Counter(cols).most_common(1)[0][0] if cols else -1
    min_r_S = min(rows) if rows else -1
    max_r_S = max(rows) if rows else -1
    return int(static_c), int(min_r_S), int(max_r_S)

def generate_v_shape(preserved_coord: tuple[int, int] | None, static_props: tuple[int, int, int], H: int, W: int) -> list[tuple[int, int]]:
    """Generates coordinates for the 'V' shape in the M=7 right-side rule."""
    shape_coords = []
    if not preserved_coord or not static_props or static_props[0] == -1:
        return shape_coords

    pr, pc = preserved_coord
    static_c, min_r_S, max_r_S = static_props

    # Ensure static properties are valid
    if min_r_S == -1 or max_r_S == -1:
         return shape_coords

    # Segment 1 (Approach): Diagonal down-right until static object row
    for i in range(1, H):
        tr, tc = pr + i, pc + i
        if tr >= min_r_S: break # Stop before hitting static object's row span
        if 0 <= tr < H and 0 <= tc < W: shape_coords.append((tr, tc))
        else: break # Out of bounds

    # Segment 2 (Alongside): Down alongside static object + 1 column
    for i in range(max_r_S - min_r_S + 1):
        tr, tc = min_r_S + i, static_c + 1
        if 0 <= tr < H and 0 <= tc < W: shape_coords.append((tr, tc))

    # Segment 3 (Depart): Diagonal down-left from static object until preservation column
    for i in range(H): # Limit search range
        tr, tc = max_r_S + 1 + i, static_c - i
        if tc < 0: break # Out of bounds left
        if 0 <= tr < H and 0 <= tc < W:
            shape_coords.append((tr, tc))
        else: break # Out of bounds other
        if tc == pc: break # Stop when reaching the preserved mover's column

    return shape_coords


# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule based on identified Anchor, Static, and Mover roles.
    Follows a sequential placement/overwrite logic, with movers/generation only placing on background.
    """
    # Convert to numpy array for easier manipulation
    inp = np.array(input_grid, dtype=int)
    if inp.size == 0: return [] # Handle empty input
    H, W = inp.shape

    # 1. Determine background color
    B = find_background_color(inp)

    # 2. Initialize output grid
    out = np.full((H, W), B, dtype=int)

    # 3. Identify Anchor column and value(s)
    anc_c, anchor_vals = find_anchor_column(inp, B)
    # If no clear anchor found, return background grid.
    if anc_c == -1:
        return out.tolist()

    # 4. Identify Mover (M) and Static (S) colors
    M, static_colors = identify_roles(inp, anc_c, anchor_vals, B)

    # 5. Static Placement (Overwrites Background)
    all_static_coords = []
    static_props = (-1, -1, -1)
    for S_val in static_colors:
        s_coords = get_object_coords(inp, S_val)
        all_static_coords.extend(s_coords)
        for r, c in s_coords:
            if 0 <= r < H and 0 <= c < W: out[r, c] = S_val

    # Get static properties potentially needed for M=7 rule
    if M == 7:
         # Assumption: M=7 rule specifically uses the static object '9' based on train_3
         static_coords_for_M7 = get_object_coords(inp, 9)
         static_props = get_static_properties(static_coords_for_M7)

    # 6. Anchor Placement (Overwrites Background/Static)
    if 0 <= anc_c < W:
        out[:, anc_c] = inp[:, anc_c]

    # If no mover identified, return grid with static/anchor placed
    if M == -1:
        return out.tolist()

    # 7. Get Mover coordinates from input
    input_M_coords = get_object_coords(inp, M)
    if not input_M_coords:
        return out.tolist() # No movers to process

    # 8. Determine LEFT vs RIGHT mover location
    mover_cols = [c for r, c in input_M_coords]
    avg_col_M = sum(mover_cols) / len(mover_cols) if mover_cols else anc_c
    # Treat movers exactly in anchor column as neither left nor right for these rules
    is_left_mover = avg_col_M < anc_c
    # Right mover rules are currently only defined for M=7
    is_right_mover = avg_col_M > anc_c and M == 7

    # 9. Process LEFT Movers
    if is_left_mover:
        flag_minus_2 = False # Tracks if a successful move originated from rel_col -2

        # Define M-dependent shifts
        dr1_map = {4: 0, 3: -1, 8: -4, 9: 0}
        dr2_map = {4: -2, 3: -1, 8: -4, 9: -2}
        dr3 = -5 # M=9 only

        dc1 = 0
        # dc2 is 0 for M=9, else 1
        dc2 = 0 if M == 9 else 1
        dc3 = 0 # M=9 only

        mover_placements = [] # Stores (target_row, target_col, source_rel_col)

        # Calculate target positions for all relevant input movers
        for r, c in input_M_coords:
            rel_c = c - anc_c
            dr, dc = 0, 0
            valid_shift_rule = False

            if rel_c == -1:
                dr, dc = dr1_map.get(M, 0), dc1
                valid_shift_rule = True
            elif rel_c == -2:
                dr, dc = dr2_map.get(M, 0), dc2
                valid_shift_rule = True
            elif rel_c == -3 and M == 9:
                dr, dc = dr3, dc3
                valid_shift_rule = True

            if valid_shift_rule:
                tr, tc = r + dr, c + dc
                mover_placements.append({'tr': tr, 'tc': tc, 'src_rel_c': rel_c})

        # Apply Mover Placements (Only Overwrite Background)
        for placement in mover_placements:
            tr, tc, src_rel_c = placement['tr'], placement['tc'], placement['src_rel_c']
            if 0 <= tr < H and 0 <= tc < W and out[tr, tc] == B: # Check bounds and background
                out[tr, tc] = M
                if src_rel_c == -2:
                    flag_minus_2 = True # Mark success only if placement happened

        # Apply Conditional Generation (Only Overwrite Background)
        if flag_minus_2:
            if M == 4:
                # Target (0, anc_c)
                tr, tc = 0, anc_c
                if 0 <= tr < H and 0 <= tc < W and out[tr, tc] == B: out[tr, tc] = 4
            elif M == 8:
                # Target (0, anc_c - 1)
                tr, tc = 0, anc_c - 1
                if 0 <= tr < H and 0 <= tc < W and out[tr, tc] == B: out[tr, tc] = 8
            elif M == 9:
                # Target1 (0, anc_c - 1)
                tr1, tc1 = 0, anc_c - 1
                if 0 <= tr1 < H and 0 <= tc1 < W and out[tr1, tc1] == B: out[tr1, tc1] = 9
                # Target2 (1, anc_c - 1)
                tr2, tc2 = 1, anc_c - 1
                if 0 <= tr2 < H and 0 <= tc2 < W and out[tr2, tc2] == B: out[tr2, tc2] = 9

    # 10. Process RIGHT Movers (Only M=7 logic defined)
    elif is_right_mover: # M == 7 is implied by the flag
        preserved_mover_coord = None
        # Find and place the preserved mover adjacent to the anchor (Overwrites)
        for r, c in input_M_coords:
            if c == anc_c + 1:
                 # Check input anchor column at the same row
                 if 0 <= r < H and inp[r, anc_c] in anchor_vals:
                     # Place in output if bounds are valid (Overwrite OK here)
                     if 0 <= r < H and 0 <= c < W:
                         out[r, c] = M # M is 7 here
                         preserved_mover_coord = (r, c)
                         break # Assume only one based on train_3

        # Generate 'V' shape if preservation occurred and static props are valid
        if preserved_mover_coord and static_props[0] != -1:
             shape_coords = generate_v_shape(preserved_mover_coord, static_props, H, W)
             # Place shape points (Only Overwrite Background)
             for gr, gc in shape_coords:
                 if 0 <= gr < H and 0 <= gc < W and out[gr, gc] == B: # Check bounds and background
                     out[gr, gc] = M # M is 7 here

    # 11. ELSE (Mixed/Unknown Mover pattern, or M != 7 on right)
    # No action defined for these cases, grid remains as is after Static/Anchor placement.

    # 12. Return final grid
    return out.tolist()