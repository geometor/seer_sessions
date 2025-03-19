"""
The transformation rule is to invert the colors of the input grid, specifically swapping blue and white pixels. Every blue pixel in the input grid becomes a white pixel in the output grid, and every white pixel in the input grid becomes a blue pixel in the output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Get the dimensions of the grid
    rows, cols = output_grid.shape

    # Iterate through each pixel in the grid
    for i in range(rows):
        for j in range(cols):
            # Swap blue and white: 1 becomes 0, and 0 becomes 1
            if output_grid[i, j] == 1:  # Blue
                output_grid[i, j] = 0  # White
            elif output_grid[i, j] == 0:  # White
                output_grid[i, j] = 1  # Blue

    return output_grid