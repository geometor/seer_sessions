"""
Transformation Rule Natural Language Description:

1. Initialize the output grid as a copy of the input grid.
2. Iterate through each row of the grid.
3. For each row, check if a red (2) pixel exists at the beginning (column 0).
4. If a red pixel is found at the beginning:
    a. Search for the first azure (8) pixel in that row, starting from column 1 up to the end of the row.
    b. If an azure (8) pixel is found at column index 'stopper_col':
        i. Fill the cells in the output grid for the current row from column 1 up to (but not including) 'stopper_col' with azure (8).
        ii. Change the pixel at 'stopper_col' in the output grid to yellow (4).
    c. If no azure (8) pixel is found in the rest of the row, make no changes to this row (it remains as copied).
    d. Proceed to the next row (do not check the right side if the left side had a red pixel).
5. If no red pixel was found at the beginning of the row (column 0), check if a red (2) pixel exists at the end (last column).
6. If a red pixel is found at the end:
    a. Search for the first azure (8) pixel in that row, scanning backwards from the second-to-last column down to column 0.
    b. If an azure (8) pixel is found at column index 'stopper_col':
        i. Fill the cells in the output grid for the current row from 'stopper_col + 1' up to (but not including) the last column with azure (8).
        ii. Change the pixel at 'stopper_col' in the output grid to yellow (4).
    c. If no azure (8) pixel is found in the rest of the row (scanning backwards), make no changes to this row (it remains as copied).
7. After checking all rows, return the modified output grid.
"""

import numpy as np

AZURE = 8
RED = 2
YELLOW = 4

def find_stopper_left(row_data, start_col, end_col):
    """Finds the index of the first azure (8) pixel from left."""
    for c in range(start_col, end_col):
        if row_data[c] == AZURE:
            return c
    return -1 # Not found

def find_stopper_right(row_data, start_col, end_col):
    """Finds the index of the first azure (8) pixel from right."""
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
    the opposite end is reached if no azure pixel is found. If a row starts
    or ends with red but contains no azure pixels, it remains unchanged.
    """
    # Initialize output_grid as a copy of input_grid
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.array(input_grid, dtype=int)
    num_rows, num_cols = output_grid.shape

    # Iterate through each row
    for r in range(num_rows):
        row_data = input_np[r, :] # Use original input row for checks

        # Check for red pixel at the left edge (priority)
        # Ensure there's at least one column to fill or check
        if num_cols > 1 and row_data[0] == RED:
            # Find the stopper from left (column 1 to num_cols - 1)
            stopper_col = find_stopper_left(row_data, 1, num_cols)

            # Only modify if a stopper was found
            if stopper_col != -1:
                # Fill with azure up to the stopper
                output_grid[r, 1:stopper_col] = AZURE
                # Replace stopper with yellow
                output_grid[r, stopper_col] = YELLOW
            # If no stopper found, the row remains unchanged (already copied)
            # If red was on the left, skip checking the right for this row
            continue

        # Check for red pixel at the right edge (only if no red on left)
        # Ensure there's at least one column to fill or check
        if num_cols > 1 and row_data[num_cols - 1] == RED:
            # Find the stopper from right (column num_cols - 2 down to 0)
            stopper_col = find_stopper_right(row_data, num_cols - 2, 0)

            # Only modify if a stopper was found
            if stopper_col != -1:
                 # Fill with azure from stopper+1 up to the right edge (exclusive)
                output_grid[r, stopper_col + 1 : num_cols - 1] = AZURE
                 # Replace stopper with yellow
                output_grid[r, stopper_col] = YELLOW
            # If no stopper found, the row remains unchanged (already copied)


    return output_grid.tolist() # Return as list of lists