```python
import numpy as np
from collections import Counter
import math

"""
The transformation rule identifies distinct roles for different non-background colors in the input grid: Anchor, Static, and Mover.

1.  **Initialization**: Determine grid dimensions (H, W) and the background color (B, typically the most frequent color). Create an output grid initialized with B.
2.  **Role Identification**:
    *   **Anchor**: Find the column (`anc_c`) containing specific, vertically consistent non-background values (`anchor_vals`). These values often form known patterns (e.g., [2], [5], [6], [2, 8]) or are the only non-background values in that column.
    *   **Mover**: Identify the most frequent non-anchor, non-background color (`M`) in the input grid.
    *   **Static**: Identify any remaining non-background, non-anchor, non-mover colors (`S`).
3.  **Sequential Placement (Overwrite Logic)**: Apply transformations in order, allowing later steps to overwrite earlier ones.
    *   **Static Placement**: Copy all Static objects (`S`) from their input positions to the output grid. Record properties (column, row span) if needed (especially for the M=7 case).
    *   **Anchor Placement**: Copy the entire anchor column (`anc_c`) from the input to the output grid.
    *   **Mover Processing**:
        *   Determine if the Mover (`M`) objects are primarily located LEFT (`< anc_c`) or RIGHT (`> anc_c`) of the anchor column based on their average column index.
        *   **Left Movers**:
            *   Apply specific vertical (`dr`) and horizontal (`dc`) shifts to movers based on `M` and their relative column (`rel_c`) to the anchor:
                *   `rel_c = -1`: Shift `(dr1(M), 0)`. `dr1` maps M={4:0, 3:-1, 8:-4, 9:0}.
                *   `rel_c = -2`: Shift `(dr2(M), dc2(M))`. `dr2` maps M={4:-2, 3:-1, 8:-4, 9:-2}. `dc2` is 0 if M=9, else 1.
                *   `rel_c = -3`: Only if M=9, shift `(-5, 0)`.
            *   Place the shifted Mover value in the output grid if the target coordinates are valid. Keep track if any successful move originated from `rel_c = -2` (`flag_minus_2`).
            *   **Conditional Generation**: If `flag_minus_2` is true, generate new Mover values at specific locations near the top of the grid, depending on `M`:
                *   M=4: Place 4 at `(0, anc_c)`.
                *   M=8: Place 8 at `(0, anc_c - 1)`.
                *   M=9: Place 9 at `(0, anc_c - 1)` and `(1, anc_c - 1)`.
        *   **Right Movers (M=7 Specific)**:
            *   Find and preserve an M=7 mover at `(r, anc_c + 1)` if `input[r, anc_c]` is an anchor value. Store its location `(pr, pc)`.
            *   If preserved, generate a 'V' shape using M=7, positioned relative to `(pr, pc)` and the properties (column, row span) of the Static objects (assumed to be S=9 based on examples). Place the shape in the output grid.
        *   **Other Movers**: Movers far left (`rel_c < -3`, unless M=9) or movers in unhandled right-side patterns are effectively removed (overwritten by background or other placements).
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
            # Prioritize known patterns
            if unique_non_bg in known_anchor_sets:
                anchor_candidates.append({'col': c, 'vals': unique_non_bg, 'priority': 1, 'count': len(non_background_values)})
            # Otherwise consider columns with only one type of non-bg value
            elif len(unique_non_bg) == 1:
                 anchor_candidates.append({'col': c, 'vals': unique_non_bg, 'priority': 2, 'count': len(non_background_values)})
            # Fallback: store any column with non-bg elements
            else:
                 anchor_candidates.append({'col': c, 'vals': unique_non_bg, 'priority': 3, 'count': len(non_background_values)})


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
             # Check if it's actually present outside the anchor column too,
             # although the main heuristic is frequency.
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
    Follows a sequential placement/overwrite logic.
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
    # If no clear anchor found, maybe return input or background?
    # Based on examples, anchor seems always present. If not, return background.
    if anc_c == -1:
        # print("Warning: No anchor column identified.")
        return out.tolist()

    # 4. Identify Mover (M) and Static (S) colors
    M, static_colors = identify_roles(inp, anc_c, anchor_vals, B)

    # If no mover found, just place static and anchor and return
    if M == -1:
        # print("Warning: No mover identified.")
        # Place Static
        for S_val in static_colors:
             static_coords = get_object_coords(inp, S_val)
             for r, c in static_coords:
                 if 0 <= r < H and 0 <= c < W: out[r, c] = S_val
        # Place Anchor
        if 0 <= anc_c < W: out[:, anc_c] = inp[:, anc_c]
        return out.tolist()

    # 5. Static Placement
    all_static_coords = []
    static_props = (-1, -1, -1)
    for S_val in static_colors:
        s_coords = get_object_coords(inp, S_val)
        all_static_coords.extend(s_coords)
        for r, c in s_coords:
            if 0 <= r < H and 0 <= c < W: out[r, c] = S_val

    # Get properties potentially needed for M=7 rule
    if M == 7:
         # Assumption: M=7 rule specifically uses the static object '9' based on train_3
         static_coords_for_M7 = get_object_coords(inp, 9)
         static_props = get_static_properties(static_coords_for_M7)
    # else: # Currently no other rule explicitly needs static props
    #    static_props = get_static_properties(all_static_coords)


    # 6. Anchor Placement (overwrites static if necessary)
    if 0 <= anc_c < W:
        out[:, anc_c] = inp[:, anc_c]

    # 7. Get Mover coordinates
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
            valid_move = False

            if rel_c == -1:
                dr, dc = dr1_map.get(M, 0), dc1 # Default dr=0 if M unknown
                valid_move = True
            elif rel_c == -2:
                dr, dc = dr2_map.get(M, 0), dc2 # Default dr=0 if M unknown
                valid_move = True
            elif rel_c == -3 and M == 9:
                dr, dc = dr3, dc3
                valid_move = True

            if valid_move:
                tr, tc = r + dr, c + dc
                mover_placements.append((tr, tc, rel_c))

        # Apply Mover Placements (overwrites anchor/static if necessary)
        for tr, tc, src_rel_c in mover_placements:
            if 0 <= tr < H and 0 <= tc < W:
                out[tr, tc] = M
                if src_rel_c == -2:
                    flag_minus_2 = True

        # Apply Conditional Generation (if triggered by a move from rel_col -2)
        if flag_minus_2:
            if M == 4:
                # Place 4 at (0, anc_c)
                if 0 <= 0 < H and 0 <= anc_c < W: out[0, anc_c] = 4
            elif M == 8:
                # Place 8 at (0, anc_c - 1)
                tc_gen = anc_c - 1
                if 0 <= 0 < H and 0 <= tc_gen < W: out[0, tc_gen] = 8
            elif M == 9:
                # Place 9 at (0, anc_c - 1) and (1, anc_c - 1)
                tc_gen = anc_c - 1
                if 0 <= 0 < H and 0 <= tc_gen < W: out[0, tc_gen] = 9
                if 0 <= 1 < H and 0 <= tc_gen < W: out[1, tc_gen] = 9

    # 10. Process RIGHT Movers (Only M=7 logic defined)
    elif is_right_mover: # M == 7 is implied by the flag
        preserved_mover_coord = None
        # Find and place the preserved mover adjacent to the anchor
        for r, c in input_M_coords:
            if c == anc_c + 1:
                 # Check input anchor column at the same row
                 if 0 <= r < H and inp[r, anc_c] in anchor_vals:
                     # Place in output if bounds are valid
                     if 0 <= r < H and 0 <= c < W:
                         out[r, c] = M # M is 7 here
                         preserved_mover_coord = (r, c)
                         break # Assume only one based on train_3

        # Generate 'V' shape if preservation occurred and static props are valid
        if preserved_mover_coord and static_props[0] != -1:
             shape_coords = generate_v_shape(preserved_mover_coord, static_props, H, W)
             for gr, gc in shape_coords:
                 # Place shape points (overwriting previous values)
                 if 0 <= gr < H and 0 <= gc < W:
                     out[gr, gc] = M # M is 7 here

    # 11. ELSE (Mixed/Unknown Mover pattern, or M != 7 on right)
    # No action defined for these cases, grid remains as is after Static/Anchor placement.

    # 12. Return final grid
    return out.tolist()
```