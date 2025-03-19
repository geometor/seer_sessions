"""
Identifies magenta (6) pixels in the input grid. Maintains the magenta pixels in the first column and moves all other magenta pixels to the first column, filling the rest with white (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Get the dimensions of the grid
    rows, cols = output_grid.shape
    
    # find all magenta pixels
    magenta_pixels = []
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 6:
                magenta_pixels.append((r,c))

    # Fill output grid with white.  This will overwrite magenta
    #   pixels that will later be moved.
    output_grid[:] = 0

    # move first column and other magenta to the left
    magenta_col = 0
    for r,c in magenta_pixels:
        output_grid[r, 0] = 6

    return output_grid