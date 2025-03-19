"""
The transformation expands the original image by surrounding each original pixel with light blue and preserving the position of the original gray.
Add additional white border to the resulting image.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = input_rows * 2, input_cols * 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)
    
    # fill new grid with 8
    output_grid[:] = 8

    # replace the original colors in the expanded grid, keeping the relative position
    for r in range(input_rows):
        for c in range(input_cols):
            output_grid[r*2, c*2] = input_grid[r,c]


    return output_grid