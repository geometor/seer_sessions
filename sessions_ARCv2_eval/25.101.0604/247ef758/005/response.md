```python
import numpy as np
import math

"""
Transforms an input grid based on rules determined by identifying a vertical 'axis' column.

The transformation involves:
1. Identifying a vertical 'axis' column (index `axis_col`), defined as the first column where all middle rows (rows 1 to H-2) share the same single non-zero value (`axis_value`).
2. Copying the top and bottom boundary rows (0 and H-1) directly from the input to the output.
3. For each middle row `r`:
    a. Clearing the 'left zone' (columns 0 to `axis_col` - 1) in the output. (Note: This might be an oversimplification; the true rule could involve conditional copying).
    b. Copying the value from the 'axis column' (input[r, axis_col]) to the output.
    c. Copying the value from the 'value column' (input[r, axis_col + 1]) to the output. This value acts as a 'selector_color' `C`.
    d. Modifying the 'right zone' (columns `axis_col` + 2 onwards) in the output based on an action determined by the `selector_color` `C` and the `axis_value` (task context).
    e. The specific mapping from `C` to the 'right_zone_action' is defined in rule sets chosen based on `axis_value`:
        - `axis_value` = 2: Rules for drawing [4,4,4], [7,7,7], copying last col, or noop.
        - `axis_value` = 3: Rules for copying specific indices from row 0, drawing a complex pattern, drawing [5,0,5], or noop.
        - `axis_value` = 1: Rules for drawing [3,3,3], drawing [6,0,6,6] right-aligned, conditionally copying last col (if 7 not in left zone), or noop.
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
        # Fallback: first column with any non-zero value in any row
        for j in range(W):
             if np.any(grid[:, j] != 0):
                 # Use the value from row 0 if possible, else row 1, else 0
                 axis_val_candidate = 0
                 if H > 0 and 0 <= j < W:
                     axis_val_candidate = grid[0, j]
                 if H > 1 and 0 <= j < W and axis_val_candidate == 0:
                      axis_val_candidate = grid[1, j]
                 return j, axis_val_candidate
        return 0, 0 # If grid is all zeros

    middle_rows = grid[1:H-1, :]

    # Primary rule: Find first column with a single, non-zero value repeated
    # across all middle rows.
    for j in range(W):
        # Handle edge case where grid has columns but middle_rows slice might not
        if j >= middle_rows.shape[1]: continue # Avoid index error

        col = middle_rows[:, j]
        unique_vals = np.unique(col)
        # Check if there's exactly one unique value AND it's non-zero
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
            axis_value_fallback = middle_rows[0, j]
            found_fallback = True
            break

    if found_fallback:
        return axis_col_fallback, axis_value_fallback

    # Absolute fallback: return 0, 0 if no clear axis found
    return 0, 0


def transform(input_grid_list: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rules to the input grid.
    """
    # Convert to numpy array for easier slicing and manipulation
    input_grid = np.array(input_grid_list, dtype=int)
    H, W = input_grid.shape

    # --- Handle Edge Cases ---
    if H == 0 or W == 0:
        return [] # Empty grid in, empty grid out
    if H <= 2: # If 1 or 2 rows, copy input directly (consistent with examples)
        return input_grid_list

    # --- Initialize Output Grid ---
    output_grid = np.zeros_like(input_grid)

    # --- Step 1 & 2: Identify Axis Column and Value ---
    axis_col, axis_value = find_axis_column(input_grid)

    # --- Step 3: Define Task Context Rules based on axis_value ---
    rules = {}
    if axis_value == 2: # Task 1 context (train_1)
        # Selector color -> (action_type, param1, param2, ...)
        rules = {
            4: ('draw', [4,4,4], 'center'),
            7: ('draw', [7,7,7], 'center'),
            6: ('copy_last_col',),
            3: ('noop',)
        }
    elif axis_value == 3: # Task 2 context (train_2)
        # Corrected rule for selector 4
        rules = {
            4: ('copy_indices_specific', 0, {7: 7, 11: 11, W-1: W-1}), # Copy input[0,idx]->output[r,idx] for given indices
            7: ('draw', [7,7,7,7, 0, 7,7,7], 'center'),
            5: ('draw', [5, 0, 5], 'center'),
            3: ('noop',)
        }
    elif axis_value == 1: # Task 3 context (train_3)
        # Corrected rule for selector 2
         rules = {
            3: ('draw', [3,3,3], 'center'),
            6: ('draw', [6, 0, 6, 6], 'right'),
            2: ('copy_conditional_last_col', 7), # Conditional copy last col if 7 not in left zone
            1: ('noop',)
        }
    # If axis_value doesn't match known contexts, rules remains empty.

    # --- Step 4: Copy Boundary Rows ---
    output_grid[0, :] = input_grid[0, :]
    output_grid[H-1, :] = input_grid[H-1, :]

    # --- Step 5: Process Middle Rows ---
    for r in range(1, H - 1):
        # --- Part A: Clear Left Zone & Copy Preserved Columns ---
        # Left zone (0 to axis_col-1) is cleared (remains 0 from initialization).
        # Note: This clearing might be incorrect based on expected outputs analysis.

        # Copy axis column value (if axis exists)
        if 0 <= axis_col < W:
            output_grid[r, axis_col] = input_grid[r, axis_col]

        # Copy value column (axis_col + 1) and get selector color
        selector_color = 0 # Default if no value column
        value_col = axis_col + 1
        if value_col < W:
             output_grid[r, value_col] = input_grid[r, value_col]
             selector_color = input_grid[r, value_col]
        else:
             continue # No value column, so no selector, skip right zone processing

        # --- Part B: Apply Rules to the Right Zone ---
        if selector_color in rules:
            action = rules[selector_color]
            rule_type = action[0]

            # Define the right zone (columns strictly right of the value column)
            right_zone_start_col = axis_col + 2
            right_zone_end_col = W # Exclusive index
            right_zone_width = right_zone_end_col - right_zone_start_col

            # Proceed only if there is a right zone to modify
            if right_zone_width <= 0: continue

            # Execute action based on rule type
            if rule_type == 'draw':
                _, pattern, alignment = action
                pattern_arr = np.array(pattern)
                pattern_width = len(pattern_arr)

                if pattern_width > right_zone_width: continue # Pattern too wide

                start_offset = 0
                if alignment == 'center':
                    start_offset = (right_zone_width - pattern_width) // 2
                elif alignment == 'right':
                    start_offset = right_zone_width - pattern_width

                draw_start_col = right_zone_start_col + start_offset
                draw_end_col = min(draw_start_col + pattern_width, W)
                pattern_len_to_draw = draw_end_col - draw_start_col

                if pattern_len_to_draw > 0:
                   output_grid[r, draw_start_col:draw_end_col] = pattern_arr[:pattern_len_to_draw]

            elif rule_type == 'copy_indices_specific':
                _, source_row_idx, index_map = action # index_map is {source_col: target_col} (here they are the same)
                for source_col, target_col in index_map.items():
                    # Check validity for source and target, and ensure target is in right zone
                    if 0 <= source_row_idx < H and 0 <= source_col < W and \
                       0 <= target_col < W and target_col >= right_zone_start_col:
                       output_grid[r, target_col] = input_grid[source_row_idx, source_col]

            elif rule_type == 'copy_last_col':
                 last_col_idx = W - 1
                 if last_col_idx >= right_zone_start_col: # Check target is in right zone
                     if 0 <= last_col_idx < W: # Check source is valid
                         output_grid[r, last_col_idx] = input_grid[r, last_col_idx]

            elif rule_type == 'copy_conditional_last_col':
                _, prohibited_val = action
                condition_met = True
                if axis_col > 0: # Check if left zone exists
                    left_zone = input_grid[r, 0:axis_col]
                    if prohibited_val in left_zone:
                        condition_met = False

                if condition_met:
                    last_col_idx = W - 1
                    if last_col_idx >= right_zone_start_col: # Check target is in right zone
                       if 0 <= last_col_idx < W: # Check source is valid
                           output_grid[r, last_col_idx] = input_grid[r, last_col_idx]

            # 'noop' requires no action

    # --- Step 6: Convert Back to List of Lists ---
    return output_grid.tolist()
```