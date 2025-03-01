"""
Keep maroon pixels, replace grey pixels with maroon, and replace all other colors with white.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid, but with all white.
    output_grid = np.zeros_like(input_grid)

    # Iterate through each cell of the input_grid
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            # If the pixel is maroon, keep as maroon in the output grid.
            if input_grid[i, j] == 9:
                output_grid[i,j] = 9
            # If the pixel is gray, keep as maroon in the output grid
            if input_grid[i, j] == 5:
                output_grid[i, j] = 9

    return output_grid