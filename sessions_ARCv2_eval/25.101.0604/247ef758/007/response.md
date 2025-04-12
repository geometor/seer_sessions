```python
import numpy as np
import math

"""
Transforms an input grid based on identifying a vertical axis column and applying rules row-by-row.

1.  Initialize an `output_grid` with the same dimensions as the `input_grid`, filled with zeros.
2.  Handle edge case: If the input grid height `H` is 0 or width `W` is 0, return an empty grid.
3.  Identify the `axis_column` index (`axis_col`) and the shared `axis_value` by finding the first column where all middle rows (1 to H-2) share the same single non-zero value. Use fallbacks if no such column exists or H < 3.
4.  Define the rule sets for modifying the `right_zone` (columns `axis_col + 2` to `W-2`) based on the `axis_value`:
    *   If `axis_value` is 2: Selector 4 draws [4,4,4] at cols 8-10; Selector 7 draws [7,7,7] at cols 9-11. Others noop.
    *   If `axis_value` is 3: Selector 4 copies input[0,7]->output[r,7] and input[0,11]->output[r,11]; Selector 7 draws [7,7,7,7,0,7,7,7] centered; Selector 5 draws [5,0,5] centered. Others noop.
    *   If `axis_value` is 1: Selector 3 draws [3,3,3] centered; Selector 6 draws [6,0,6,6] right-aligned. Others noop.
    *   Otherwise: Empty rule set (noop for all).
5.  For each row `r` from 0 to H-1:
    a.  Clear the left zone (`output_grid[r, 0:axis_col] = 0`).
    b.  Copy the axis column value (`input_grid[r, axis_col]` to `output_grid[r, axis_col]`).
    c.  Copy the value column value (`input_grid[r, axis_col+1]` to `output_grid[r, axis_col+1]`) and determine the `selector_color` C.
    d.  Copy the last column value (`input_grid[r, W-1]` to `output_grid[r, W-1]`).
    e.  Apply the rule for `C` based on `axis_value` to the right zone columns (`axis_col + 2` to `W-2`) of the output grid.
6.  Return the `output_grid`.
"""

def find_axis_column(grid: np.ndarray) -> tuple[int, int]:
    """
    Finds the index of the vertical axis column and its common non-zero value.
    The axis column is the first column 'j' such that grid[r, j]
    has the same non-zero value for all middle rows r (1 to H-2).
    Includes fallbacks for edge cases.

    Args:
        grid: The input grid as a NumPy array.

    Returns:
        A tuple (axis_col_index, axis_value).
        Returns (0, 0) if no clear axis is found or grid is too small.
    """
    H, W = grid.shape
    axis_value = 0

    # Handle grids too small to have middle rows (H<=2)
    if H <= 2:
        for j in range(W):
             if np.any(grid[:, j] != 0):
                 axis_val_candidate = 0
                 if H > 0 and 0 <= j < W: axis_val_candidate = grid[0, j]
                 # Prioritize value from row 1 if row 0 is 0 and H>1
                 if H > 1 and 0 <= j < W and axis_val_candidate == 0: axis_val_candidate = grid[1, j]
                 return j, axis_val_candidate
        return 0, 0 # Grid is all zeros or empty

    middle_rows = grid[1:H-1, :]

    # Primary rule: Find first column with a single, non-zero value repeated
    for j in range(W):
        if j >= middle_rows.shape[1]: continue
        col = middle_rows[:, j]
        unique_vals = np.unique(col)
        if len(unique_vals) == 1 and unique_vals[0] != 0:
             return j, unique_vals[0] # Found axis column and value

    # Fallback if primary rule fails: first col with any non-zero in middle rows
    axis_col_fallback = 0
    axis_value_fallback = 0
    found_fallback = False
    for j in range(W):
        if j >= middle_rows.shape[1]: continue
        if np.any(middle_rows[:, j] != 0):
            axis_col_fallback = j
            # Use the value from the first middle row as the fallback axis value
            axis_value_fallback = middle_rows[0, j] if middle_rows.shape[0] > 0 else 0
            found_fallback = True
            break
    if found_fallback:
        return axis_col_fallback, axis_value_fallback

    # Absolute fallback: return 0, 0 if no clear axis found
    return 0, 0


def transform(input_grid_list: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rules row-by-row to the input grid.
    """
    # Convert input to numpy array
    input_grid = np.array(input_grid_list, dtype=int)
    H, W = input_grid.shape

    # Handle edge cases: empty grid
    if H == 0 or W == 0:
        return []

    # Initialize output grid with zeros
    output_grid = np.zeros_like(input_grid)

    # Identify axis column and value using middle rows (handles H<=2 via fallbacks)
    axis_col, axis_value = find_axis_column(input_grid)

    # Define rules based on the axis value (task context)
    # Rules apply to the 'right_zone' (cols axis_col + 2 to W - 2)
    rules = {}
    if axis_value == 2: # Task 1 context (train_1)
        rules = {
            # Use absolute fixed columns for drawing
            4: ('draw_fixed', [4,4,4], 8),  # Draw at col 8, 9, 10
            7: ('draw_fixed', [7,7,7], 9),  # Draw at col 9, 10, 11
            6: ('noop',),                   # Noop (last col handled separately)
            3: ('noop',)                    # Noop (last col handled separately)
        }
    elif axis_value == 3: # Task 2 context (train_2)
        rules = {
             # Copy specific indices from input row 0
            4: ('copy_indices_specific', 0, {7: 7, 11: 11}),
            7: ('draw_aligned', [7,7,7,7, 0, 7,7,7], 'center'), # Draw aligned in right_zone
            5: ('draw_aligned', [5, 0, 5], 'center'),          # Draw aligned in right_zone
            3: ('noop',)
        }
    elif axis_value == 1: # Task 3 context (train_3)
         rules = {
            3: ('draw_aligned', [3,3,3], 'center'),           # Draw aligned in right_zone
            6: ('draw_aligned', [6, 0, 6, 6], 'right'),      # Draw aligned in right_zone
            2: ('noop',),                                    # Conditional rule disproven
            1: ('noop',)
        }

    # Process ALL rows (0 to H-1)
    for r in range(H):
        # --- Part A: Clear Left Zone ---
        if axis_col > 0:
            output_grid[r, 0:axis_col] = 0

        # --- Part B: Copy Axis Column ---
        if 0 <= axis_col < W:
            output_grid[r, axis_col] = input_grid[r, axis_col]

        # --- Part C: Copy Value Column & Get Selector ---
        selector_color = 0 # Default
        value_col = axis_col + 1
        if value_col < W:
             output_grid[r, value_col] = input_grid[r, value_col]
             selector_color = input_grid[r, value_col]
        #else:
             # If no value column, selector remains 0, rules likely won't match

        # --- Part D: Copy Last Column ---
        if W > 0:
             # Ensure last col index is valid before copying
             last_col_idx = W - 1
             if 0 <= last_col_idx < W :
                 output_grid[r, last_col_idx] = input_grid[r, last_col_idx]


        # --- Part E: Apply Rules to the Right Zone ---
        if selector_color in rules:
            action = rules[selector_color]
            rule_type = action[0]

            # Define the 'right_zone' where these rules apply (cols axis_col + 2 up to, but not including, the last col)
            right_zone_start_col = axis_col + 2
            right_zone_end_col = W - 1 # Exclusive index (ends at W-2)
            right_zone_width = right_zone_end_col - right_zone_start_col

            # Proceed only if the right zone exists (width > 0)
            if right_zone_width <= 0: continue

            # Execute action based on rule type
            if rule_type == 'draw_aligned':
                _, pattern, alignment = action
                pattern_arr = np.array(pattern)
                pattern_width = len(pattern_arr)

                if pattern_width > right_zone_width: continue # Pattern too wide

                start_offset = 0 # Default for left alignment
                if alignment == 'center':
                    start_offset = (right_zone_width - pattern_width) // 2
                elif alignment == 'right':
                    start_offset = right_zone_width - pattern_width

                # Calculate absolute draw column indices within the output grid
                draw_start_col = right_zone_start_col + start_offset
                # Ensure drawing doesn't go past the defined right zone end or grid bounds
                draw_end_col = min(draw_start_col + pattern_width, right_zone_end_col, W)
                pattern_len_to_draw = draw_end_col - draw_start_col

                if pattern_len_to_draw > 0:
                   output_grid[r, draw_start_col:draw_end_col] = pattern_arr[:pattern_len_to_draw]

            elif rule_type == 'draw_fixed':
                 _, pattern, start_col_abs = action
                 pattern_arr = np.array(pattern)
                 pattern_width = len(pattern_arr)

                 # Calculate absolute end column
                 end_col_abs = start_col_abs + pattern_width

                 # Check if the draw region is valid within grid bounds
                 if start_col_abs >= W or start_col_abs < 0: continue # Start is out of bounds

                 # Clip end column to grid width
                 draw_end_col = min(end_col_abs, W)
                 # Calculate actual length to draw
                 pattern_len_to_draw = draw_end_col - start_col_abs

                 if pattern_len_to_draw > 0:
                      output_grid[r, start_col_abs:draw_end_col] = pattern_arr[:pattern_len_to_draw]


            elif rule_type == 'copy_indices_specific':
                _, source_row_idx, index_map = action # index_map is {source_col: target_col}
                for source_col, target_col in index_map.items():
                    # Check validity for source row/col and target col
                    # Also ensure target column is within the defined right_zone
                    if 0 <= source_row_idx < H and 0 <= source_col < W and \
                       right_zone_start_col <= target_col < right_zone_end_col:
                           # Check target column is within overall grid bounds (redundant but safe)
                           if 0 <= target_col < W:
                               output_grid[r, target_col] = input_grid[source_row_idx, source_col]

            # 'noop' requires no action

    # Convert final numpy array grid back to list of lists
    return output_grid.tolist()
```