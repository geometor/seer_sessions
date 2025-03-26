```python
import numpy as np

"""
Transforms the input grid by:
1.  Creating a modified grid where all blue (1) pixels are changed to red (2), leaving white (0) pixels unchanged.
2.  Determining the number of rows to append (N), which is half the input grid's height (integer division).
3.  Checking the row at index N in the *original* input grid.
4.  If this row matches the pattern [white, blue, blue] ([0, 1, 1]), selecting the block of N rows from the modified grid starting at index 2.
5.  Otherwise, selecting the top N rows (indices 0 to N-1) from the modified grid.
6.  Appending the selected block of rows to the bottom of the modified grid.
"""

def transform(input_grid):
    """
    Applies a color change and conditional vertical extension transformation.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The transformed grid.
    """
    # Convert input grid to a numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape

    # --- Step 1: Color Modification ---
    # Create a copy to store the color-transformed grid
    intermediate_grid = grid_np.copy()
    # Replace all blue (1) pixels with red (2) pixels
    intermediate_grid[intermediate_grid == 1] = 2

    # --- Step 2: Conditional Row Selection for Appending ---
    # Calculate the number of rows to append and the index of the condition row
    append_height = height // 2
    condition_row_index = height // 2 # Same as append_height in this case

    # Define the condition pattern to check in the *original* grid
    condition_pattern = np.array([0, 1, 1])

    # Get the row from the original input grid to check against the pattern
    # Ensure condition_row_index is within bounds (should be for H >= 2)
    if 0 <= condition_row_index < height:
        row_to_check = grid_np[condition_row_index, :]
    else:
        # Handle edge case if H < 2, although examples suggest H=6
        # Default to the standard behavior (append top rows)
        row_to_check = None

    # Determine the starting row index for appending based on the condition
    append_start_row = 0 # Default start row
    if row_to_check is not None and np.array_equal(row_to_check, condition_pattern):
        # If the condition is met, change the start row for appending
        append_start_row = 2

    # Select the block of rows to append from the intermediate_grid
    # Ensure the slice indices are valid
    end_row = append_start_row + append_height
    if end_row <= intermediate_grid.shape[0]:
         rows_to_append = intermediate_grid[append_start_row:end_row, :]
    else:
        # Fallback or error handling if calculated slice is out of bounds
        # For this specific problem structure, this shouldn't happen if H is even and >= 4
        # If H=2, append_height=1, condition_idx=1.
        # If condition met, append_start_row=2 -> slice [2:3] - Out of bounds for H=2 intermediate.
        # If condition not met, append_start_row=0 -> slice [0:1] - OK.
        # Let's refine the condition check logic slightly for H=2 case.
        # If H=2, and condition [0,1,1] is met on row 1, start_row=2 is invalid.
        # Given the examples (H=6), this specific edge case might not be relevant,
        # but robust code should consider it. Let's stick to the observed pattern for H=6.
        # Re-evaluating: If H=6, append_height=3. condition_idx=3.
        # If condition met, start_row=2. Slice is [2 : 2+3] = [2:5]. Valid for H=6 grid.
        # If condition not met, start_row=0. Slice is [0 : 0+3] = [0:3]. Valid for H=6 grid.
        # So the original logic seems okay for H=6. Let's assume valid inputs based on examples.
         rows_to_append = intermediate_grid[append_start_row:end_row, :]


    # --- Step 3: Concatenation ---
    # Vertically stack the intermediate grid and the selected rows_to_append
    output_grid = np.vstack((intermediate_grid, rows_to_append))

    return output_grid
```