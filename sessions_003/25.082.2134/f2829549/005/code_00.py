"""
1.  **Identify Key Column:** Find the column index in the input grid that contains the value '1' (blue). This is the "key column".

2.  **Create Output Grid:** Create an output grid with the same number of rows as the input grid and a fixed width of 3 columns.

3.  **Process Each Row:** For each row in the input grid:
    *   Examine the cell in the input grid at the "key column" index.
        *   If the value in the key column is '1', then check for non-zero neighbors:
            *  If the value to the *left* of the key column is within bounds and is not 0, set the output value for the row at index 0 to '3' (green).
            *  Always set the output value for the row at index 1 to '3'.
            *  If the value to the *right* of the key column is within bounds and is not 0, set the output value for the row at index 2 to '3' (green).
        *   If the row does *not* contain '1' in the key column:
            * If the value one position to the left of the key column is non-zero, set the output for that row at index 0 to 3.
            * If the value one position to the right of the key column is non-zero, set the output for that row at index 2 to 3.

4. Set all the other cells of the output grid that weren't set by the logic above, to value `0`.
"""

import numpy as np

def find_key_column(grid):
    # Find the column index that contains the value 1
    for j in range(grid.shape[1]):
        if 1 in grid[:, j]:
            return j
    return -1  # Should not happen if 1 is guaranteed

def transform(input_grid):
    # Initialize output_grid
    rows = input_grid.shape[0]
    cols = 3
    output_grid = np.zeros((rows, cols), dtype=int)
    
    # Find the key column
    key_column_index = find_key_column(input_grid)

    # Populate output_grid
    for i in range(rows):
        # Check if the key column contains '1' in the current row
        if input_grid[i, key_column_index] == 1:
            output_grid[i, 1] = 3  # Always set the middle column to 3

            # Check left neighbor
            left_neighbor_index = key_column_index - 1
            if 0 <= left_neighbor_index < input_grid.shape[1] and input_grid[i, left_neighbor_index] != 0:
                output_grid[i, 0] = 3

            # Check right neighbor
            right_neighbor_index = key_column_index + 1
            if 0 <= right_neighbor_index < input_grid.shape[1] and input_grid[i, right_neighbor_index] != 0:
                output_grid[i, 2] = 3
        else:
            # Handle cases where the current row doesn't have '1' in the key column

             # Check left neighbor
            left_neighbor_index = key_column_index - 1
            if 0 <= left_neighbor_index < input_grid.shape[1] and input_grid[i, left_neighbor_index] != 0:
                output_grid[i, 0] = 3
            
            # Check right neighbor
            right_neighbor_index = key_column_index + 1
            if 0 <= right_neighbor_index < input_grid.shape[1] and input_grid[i, right_neighbor_index] != 0:
                output_grid[i, 2] = 3


    return output_grid