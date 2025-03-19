"""
Copy the input grid to the output grid. For each column in the input grid, check if it contains any black pixels. If a column contains a black pixel, place a yellow pixel in the same column of the last row of the output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each column of the input grid
    for col in range(cols):
        # Check if the current column contains any black pixels (value 0)
        if 0 in input_grid[:, col]:
            # If black pixel is present, add a yellow pixel (value 4) to the last row of the same column
            output_grid[rows - 1, col] = 4

    return output_grid