```python
import copy

"""
Processes a 2D grid of integers column by column. 
For each column:
1. Finds all non-zero values.
2. If fewer than two non-zero values exist, the column remains unchanged.
3. If two or more non-zero values exist:
   a. Identifies the minimum non-zero value (`min_val`) in the column.
   b. Finds the row index (`trigger_row`) of the *first* occurrence of `min_val`.
   c. For all rows *below* `trigger_row`, any non-zero value in that column is replaced with `min_val`. 
   d. Values at or above `trigger_row`, and all zero values, remain unchanged.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the column-based transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input 2D grid of integers.

    Returns:
        A new list of lists representing the transformed grid.
    """
    # Handle empty grid case
    if not input_grid or not input_grid[0]:
        return []

    # Get grid dimensions
    num_rows = len(input_grid)
    num_cols = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input
    # This ensures unchanged cells/columns are correctly preserved
    output_grid = copy.deepcopy(input_grid)

    # Iterate through each column index
    for c_idx in range(num_cols):
        # --- Find non-zero elements and their locations in the current column ---
        non_zero_info = [] # List to store tuples of (value, row_index)
        for r_idx in range(num_rows):
            value = input_grid[r_idx][c_idx]
            if value != 0:
                non_zero_info.append((value, r_idx))

        # --- Check if transformation is needed (at least two non-zeros) ---
        if len(non_zero_info) < 2:
            # If less than 2 non-zeros, this column remains unchanged (already copied)
            continue

        # --- Determine the minimum non-zero value ---
        # Extract just the values from non_zero_info
        non_zero_values = [val for val, r_idx in non_zero_info]
        min_val = min(non_zero_values)

        # --- Find the first row index where the minimum value occurs ---
        trigger_row = -1 # Initialize trigger_row
        for val, r_idx in non_zero_info:
            if val == min_val:
                trigger_row = r_idx
                break # Stop at the first occurrence

        # Ensure trigger_row was found (should always happen if len >= 2)
        if trigger_row == -1: 
             # This case should technically not be reached if len(non_zero_info) >= 2
             # but included for robustness
             continue

        # --- Apply the transformation to rows below the trigger row ---
        # Iterate through rows starting from the one *after* the trigger row
        for r_idx in range(trigger_row + 1, num_rows):
            # Check if the *original* value at this position was non-zero
            if input_grid[r_idx][c_idx] != 0:
                # If it was non-zero, update the corresponding cell in the output grid
                output_grid[r_idx][c_idx] = min_val
            # If the original value was zero, it remains zero (already copied)

    # Return the modified grid
    return output_grid
```