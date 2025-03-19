"""
Change all maroon (9) pixels in the input grid to red (2) pixels. The dimensions of the grid remain the same.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Create a copy of the input array to serve as the output grid.  This ensures
    # that the dimensions are the same.
    output_grid = np.copy(input_array)

    # Iterate through all cells in the grid.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # If the cell is maroon (9), change it to red (2).
            if output_grid[i, j] == 9:
                output_grid[i, j] = 2

    return output_grid.tolist()