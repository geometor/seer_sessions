"""
The last non-zero pixel in each row of the input grid is moved to the last column of the output grid in the corresponding row.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Get the number of rows and columns
    num_rows = input_grid.shape[0]
    num_cols = input_grid.shape[1]

    # Iterate through each row
    for i in range(num_rows):
        # Find the right-most non-zero pixel in the current row
        row = input_grid[i, :]
        non_zero_indices = np.nonzero(row)[0]

        # set all non-zero pixels in the row to zero in the output grid,
        # preparing for moving right most non-zero to final col
        if len(non_zero_indices) > 0:
            output_grid[i,:] = 0

        if len(non_zero_indices) > 0:
            last_non_zero_index = non_zero_indices[-1]
            last_non_zero_value = row[last_non_zero_index]

            # Set the last cell of the corresponding row in output_grid to this value
            output_grid[i, -1] = last_non_zero_value

    return output_grid