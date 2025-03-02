"""
1.  White Pixels: If a pixel is white (0), it remains white (0) in the output grid.
2.  Blue Pixels: If a pixel is blue (1), it changes to red(2).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Iterate through each pixel of the input grid.
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            # White Pixels
            if input_grid[r,c] == 0:
                output_grid[r,c] = 0
            # Blue Pixels
            elif input_grid[r,c] == 1:
                output_grid[r,c] = 2

    return output_grid