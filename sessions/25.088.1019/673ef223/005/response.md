```python
import numpy as np

"""
Transformation Rule Natural Language Description:

1. Initialize the output grid as an identical copy of the input grid.
2. Iterate through each row of the grid. Let the number of columns be `num_cols`.
3. **Check Left Edge:** For the current row, check if the pixel at column 0 is red (2).
4. **Process Left Edge Trigger:** If the pixel at column 0 is red (2):
    a. Search for the first azure (8) pixel in that row, scanning from column 1 up to `num_cols - 1`.
    b. **Stopper Found (Left):** If an azure (8) pixel is found at column index `stopper_col`:
        i. Fill the cells in the output grid for the current row from column 1 up to (but not including) `stopper_col` with azure (8).
        ii. Change the pixel at `stopper_col` in the output grid to yellow (4).
    c. **Stopper Not Found (Left):** If no azure (8) pixel is found in the row (from column 1 onwards):
        i. Fill the cells in the output grid for the current row from column 1 up to `num_cols - 1` (inclusive) with azure (8).
    d. Proceed to the next row (do not check the right edge for this row).
5. **Check Right Edge:** If the pixel at column 0 was *not* red (2), check if the pixel at the last column (`num_cols - 1`) is red (2).
6. **Process Right Edge Trigger:** If the pixel at the last column (`num_cols - 1`) is red (2):
    a. Search for the first azure (8) pixel in that row, scanning backwards from column `num_cols - 2` down to column 0.
    b. **Stopper Found (Right):** If an azure (8) pixel is found at column index `stopper_col`:
        i. Fill the cells in the output grid for the current row from column `stopper_col + 1` up to (but not including) `num_cols - 1` with azure (8).
        ii. Change the pixel at `stopper_col` in the output grid to yellow (4).
    c. **Stopper Not Found (Right):** If no azure (8) pixel is found in the row (scanning backwards from `num_cols - 2` down to 0):
        i. Fill the cells in the output grid for the current row from column 0 up to (but not including) `num_cols - 1` with azure (8).
7. After checking and potentially modifying all rows, return the final output grid.
"""

AZURE = 8
RED = 2
YELLOW = 4

def find_stopper_left(row_data, start_col, end_col):
    """
    Finds the index of the first azure (8) pixel in a slice of a row,
    searching from left to right.
    Args:
        row_data: The numpy array representing the row.
        start_col: The starting column index (inclusive) for the search.
        end_col: The ending column index (exclusive) for the search.
    Returns:
        The column index of the first azure pixel, or -1 if not found.
    """
    for c in range(start_col, end_col):
        if row_data[c] == AZURE:
            return c
    return -1 # Not found

def find_stopper_right(row_data, start_col, end_col):
    """
    Finds the index of the first azure (8) pixel in a slice of a row,
    searching from right to left.
    Args:
        row_data: The numpy array representing the row.
        start_col: The starting column index (inclusive) for the search (usually num_cols - 2).
        end_col: The ending column index (inclusive) for the search (usually 0).
    Returns:
        The column index of the first azure pixel, or -1 if not found.
    """
    # Iterate backwards from start_col down to end_col (inclusive)
    for c in range(start_col, end_col - 1, -1):
        if row_data[c] == AZURE:
            return c
    return -1 # Not found

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    For rows starting or ending with red, draws horizontal azure lines
    inward until an azure pixel is hit (which turns yellow), or until
    the opposite end is reached if no azure pixel is found (filling the
    rest of the row with azure).
    """
    # Initialize output_grid as a copy of input_grid using numpy
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.array(input_grid, dtype=int)
    num_rows, num_cols = output_grid.shape

    # Iterate through each row
    for r in range(num_rows):
        # Get the original input row data for checks
        row_data = input_np[r, :]

        # Check for red pixel at the left edge (priority)
        # Ensure there's at least one column *next* to the red pixel to potentially fill
        if num_cols > 1 and row_data[0] == RED:
            # Find the stopper from left (column 1 to num_cols - 1)
            stopper_col = find_stopper_left(row_data, 1, num_cols)

            if stopper_col != -1:
                # Stopper found: Fill with azure up to the stopper
                output_grid[r, 1:stopper_col] = AZURE
                # Replace stopper with yellow
                output_grid[r, stopper_col] = YELLOW
            else:
                # No stopper found: Fill the rest of the row with azure
                output_grid[r, 1:num_cols] = AZURE

            # If red was on the left, skip checking the right for this row
            continue

        # Check for red pixel at the right edge (only if no red on left)
        # Ensure there's at least one column *before* the red pixel to potentially fill
        if num_cols > 1 and row_data[num_cols - 1] == RED:
            # Find the stopper from right (column num_cols - 2 down to 0)
            stopper_col = find_stopper_right(row_data, num_cols - 2, 0)

            if stopper_col != -1:
                 # Stopper found: Fill with azure from stopper+1 up to the right edge (exclusive)
                output_grid[r, stopper_col + 1 : num_cols - 1] = AZURE
                 # Replace stopper with yellow
                output_grid[r, stopper_col] = YELLOW
            else:
                 # No stopper found: Fill the rest of the row (from col 0 up to, but not including, the last col) with azure
                 output_grid[r, 0 : num_cols - 1] = AZURE

    # Return the modified grid as a list of lists
    return output_grid.tolist()
```