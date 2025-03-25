"""
The transformation rule involves mirroring the input grid vertically across the center horizontal line. Every non-white pixel in the input grid is copied to its mirrored position in the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Mirror each pixel vertically
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:  # if not white
                mirror_r = rows - 1 - r  # Calculate mirrored row index
                output_grid[mirror_r, c] = input_grid[r, c]  # Copy color to mirrored position

    return output_grid.tolist()