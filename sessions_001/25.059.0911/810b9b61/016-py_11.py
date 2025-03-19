"""
The transformation rule identifies the location of blue (1) pixels in the input grid and extends a line of green (3) pixels downwards from each blue pixel to the bottom of the grid. If a blue pixel is at the top, extend green to the bottom.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through all pixels
    for r in range(rows):
        for c in range(cols):
            # Check if the current pixel is blue (1)
            if input_grid[r, c] == 1:
                # Extend green (3) downwards from the blue pixel
                for i in range(r, rows):
                    output_grid[i, c] = 3

    return output_grid