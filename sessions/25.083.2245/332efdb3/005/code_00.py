"""
Transforms an input grid of all black pixels into a grid where even-indexed rows are all blue, and odd-indexed rows alternate between blue and black, starting with blue.
"""

import numpy as np

def transform(input_grid):
    # Create a copy of the input grid to modify.
    output_grid = np.copy(input_grid)

    # Get the dimensions of the grid.
    rows, cols = output_grid.shape

    # Iterate through each row.
    for i in range(rows):
        # Check if the row index is odd.
        if i % 2 != 0:
            # Alternate between blue (1) and black (0), starting with blue.
            for j in range(cols):
                if j % 2 == 0:
                    output_grid[i, j] = 1  # Blue
                else:
                    output_grid[i, j] = 0  # Black
        else:
            # Fill the entire row with blue (1).
            output_grid[i, :] = 1

    return output_grid