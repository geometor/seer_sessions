import numpy as np
from collections import Counter
import math

"""
The transformation rule is conditional, determined by the relative vertical positions of the topmost non-background pixels in the two rightmost columns containing non-background pixels.

1.  Identify the background color (`bg`), the rightmost column with non-background pixels (`C1`), and the second rightmost (`C2`).
2.  Find the topmost non-background pixel in `C1` (Value `V1` at row `R1`) and in `C2` (Value `V2` at row `R2`).
3.  **Condition Check:** If both `R1` and `R2` are found AND `R1 < R2`, apply the 'H11c' rule. Otherwise, apply the 'H_DownProp' rule.

**H11c Rule (R1 < R2):**
   - Initialize the output grid with `bg`.
   - Process column `C1`: Copy non-`bg` pixels from input `C1`. Fill `bg` pixels in output `C1` *above* `R1` with `V2`.
   - Process column `C2`: Copy non-`bg` pixels from input `C2`. Fill `bg` pixels in output `C2` *above* `R2` with `V2`, but only if the cell `(r, C1)` in the *output* is `bg` OR the cell `(r, C1)` in the *input* was `V1`.
   - All other output columns remain `bg`.

**H_DownProp Rule (R1 >= R2 or C2/R1/R2 not found):**
   - Initialize the output grid as a copy of the input grid.
   - For every cell `(r, c)` in the output grid: If it's `bg`, search downwards in the *input* column `c` starting from row `r+1`. If a non-`bg` pixel is found at row `r'`, set `output[r, c]` to the value of `input[r', c]`. If no non-`bg` pixel is found below, it remains `bg`. This propagation happens independently for each column.
"""

# --- Helper Functions ---

def find_background_color(grid: np.ndarray) -> int:
    """Finds the background color (most frequent, prioritizing 0 if dominant)."""
    counts = Counter(grid.flatten())
    if not counts: return 0
    if grid.size > 0:
        zero_count = counts.get(0, 0)
        # Safely get most common element, default to (0,0) if counts is empty
        most_frequent_color, most_frequent_count = counts.most_common(1)[0] if counts else (0, 0)
        # Prioritize 0 if it's most frequent or covers > 50%
        if zero_count == most_frequent_count or zero_count > grid.size * 0.5:
             background_color = 0
        else:
             background_color = most_frequent_color
    else:
        background_color = 0
    return background_color

def find_target_columns(grid: np.ndarray, background_color: int) -> tuple[int | None, int | None]:
    """Finds indices C1 (rightmost) and C2 (second rightmost) with non-bg pixels."""
    rows, cols = grid.shape
    non_bg_cols = set()
    if grid.size == 0: return None, None
    for c in range(cols):
        if np.any(grid[:, c] != background_color):
            non_bg_cols.add(c)
    sorted_cols = sorted(list(non_bg_cols))
    C1 = sorted_cols[-1] if sorted_cols else None
    C2 = sorted_cols[-2] if len(sorted_cols) > 1 else None
    return C1, C2

def find_topmost_non_background(grid: np.ndarray, col_idx: int | None, background_color: int) -> tuple[int | None, int | None]:
    """Finds row R_top and value V_top of the topmost non-bg pixel in col_idx."""
    if col_idx is None or col_idx < 0 or col_idx >= grid.shape[1]: return None, None
    height = grid.shape[0]
    column_data = grid[:, col_idx]
    non_bg_indices = np.where(column_data != background_color)[0]
    if non_bg_indices.size == 0: return None, None
    R_top = non_bg_indices[0]
    V_top = grid[R_top, col_idx]
    return R_top, V_top

def apply_h11c_transformation(input_np: np.ndarray, bg: int, C1: int, R1: int, V1: int, C2: int, R2: int, V2: int) -> np.ndarray:
    """Applies the H11c transformation logic."""
    height, width = input_np.shape
    output_np = np.full_like(input_np, bg)
    
    # Determine fill values, defaulting to bg if V2 is None (shouldn't happen if R2 is not None, but safety check)
    fill_val_for_c1_gaps = V2 if V2 is not None else bg
    fill_val_for_c2_gaps = V2 if V2 is not None else bg

    # Process column C1
    for r in range(height):
        V_current_C1 = input_np[r, C1]
        if V_current_C1 != bg:
            output_np[r, C1] = V_current_C1
        elif R1 is not None and r < R1: # R1 should not be None here based on calling condition
            output_np[r, C1] = fill_val_for_c1_gaps

    # Process column C2
    if C2 is not None and R2 is not None: # R2 should not be None here based on calling condition
        for r in range(height):
            V_current_C2 = input_np[r, C2]
            if V_current_C2 != bg:
                output_np[r, C2] = V_current_C2
            elif r < R2:
                # Condition: (output[r, C1] == bg) OR (input[r, C1] == V1)
                condition_met = False
                if output_np[r, C1] == bg:
                    condition_met = True
                # V1 should not be None if R1 is not None
                elif R1 is not None and V1 is not None and input_np[r, C1] == V1: 
                     condition_met = True

                if condition_met:
                    output_np[r, C2] = fill_val_for_c2_gaps
                    
    return output_np

def apply_h_downprop_transformation(input_np: np.ndarray, bg: int) -> np.ndarray:
    """Applies the H_DownProp transformation logic (propagate first non-bg pixel downwards)."""
    height, width = input_np.shape
    output_np = input_np.copy() # Start with a copy

    for c in range(width):
        # Find the value to propagate downwards for this column
        propagate_val = None
        # Iterate upwards to find the first non-bg value that *would* be propagated down
        # This is complex. Let's rethink.
        # Alternative: Iterate downwards, keeping track of the last non-bg value seen.
        
        # Correct DownProp: iterate each cell, if bg, look down *in input*
        for r in range(height):
            if output_np[r, c] == bg: # Check the current output cell state
                # Search downwards in the *original input* column starting from r+1
                found_val = None
                for r_look in range(r + 1, height):
                    if input_np[r_look, c] != bg:
                        found_val = input_np[r_look, c]
                        break # Found the first non-bg value below
                
                # If a value was found below, update the output cell
                if found_val is not None:
                    output_np[r, c] = found_val
                    
    return output_np

# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on a conditional rule determined by the
    relative positions of the topmost non-background pixels in the two
    rightmost non-background columns (C1, C2).
    If R1 < R2, applies H11c rule. Otherwise, applies H_DownProp rule.
    """
    input_np = np.array(input_grid, dtype=int)
    if input_np.size == 0:
        return []
    height, width = input_np.shape

    # Step 1: Determine background color
    bg = find_background_color(input_np)

    # Step 2 & 3: Find target columns C1 and C2
    C1, C2 = find_target_columns(input_np, bg)

    # If no non-background pixels exist at all, return original grid
    if C1 is None:
        return input_grid

    # Step 4 & 5: Find topmost pixels R1, V1 and R2, V2
    R1, V1 = find_topmost_non_background(input_np, C1, bg)
    R2, V2 = find_topmost_non_background(input_np, C2, bg)

    # Step 6: Conditional Check
    apply_h11c = False
    if R1 is not None and R2 is not None and R1 < R2:
        apply_h11c = True

    # Step 7 or 8: Apply the chosen transformation
    if apply_h11c:
        # We are sure R1, V1, R2, V2, C1, C2 are not None here
        output_np = apply_h11c_transformation(input_np, bg, C1, R1, V1, C2, R2, V2)
    else:
        output_np = apply_h_downprop_transformation(input_np, bg)

    # Step 9: Return result as list of lists
    return output_np.tolist()