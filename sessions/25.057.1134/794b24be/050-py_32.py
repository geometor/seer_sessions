"""
Iterate through each pixel of the input grid. If the pixel's value is 0 (white), keep the value as 0 (white) in the corresponding position in the output grid. If the pixel's value is 1 (blue), change the value to 2 (red) in the corresponding position in the output grid. The output grid should be the same shape as the input.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Iterate through each pixel of the input grid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # If the pixel's value is 1 (blue), change it to 2 (red)
            if output_grid[i, j] == 1:
                output_grid[i, j] = 2

    return output_grid