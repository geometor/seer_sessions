"""
Identify maroon and grey pixels in the input grid. Preserve maroon pixels in the output grid, and change grey pixels to maroon. Change all other color pixels to white.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input, but all white
    output_grid = np.zeros_like(input_grid)

    # Iterate through each cell of the input_grid
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            # If the pixel is maroon, keep it as maroon in the output grid.
            if input_grid[i, j] == 9:
                output_grid[i, j] = 9
            # If the pixel is gray, change to maroon in the output grid.
            elif input_grid[i, j] == 5:
                output_grid[i, j] = 9
            # Otherwise, change to white
            else:
                output_grid[i,j] = 0

    return output_grid