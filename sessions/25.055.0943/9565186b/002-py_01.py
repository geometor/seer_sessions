"""
Iterate through each pixel in the input grid.  If the pixel is red (2), keep its color unchanged in the output grid. If the pixel is blue (1) or azure (8), change its color to gray (5) in the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Iterate through each cell of the grid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # If the pixel is blue or azure, change it to gray
            if output_grid[i, j] == 1 or output_grid[i, j] == 8:
                output_grid[i, j] = 5

    return output_grid