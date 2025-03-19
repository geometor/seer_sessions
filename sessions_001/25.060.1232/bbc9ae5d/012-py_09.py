"""
The transformation rule identifies the first non-zero pixel in the input grid and uses its color and row index to create a triangle in the output grid. The output grid has the same number of rows as the input grid. The triangle starts at the top-left corner (0, 0) and expands downwards and to the right. The number of rows in the triangle, and thus the width of its base, is determined by the row index of the first non-zero pixel in the input grid plus one.
"""

import numpy as np

def get_first_nonzero(grid):
    # return first non zero element of grid and its row index
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
             if grid[r,c] != 0: return grid[r,c], r
    return 0, -1

def transform(input_grid):
    # initialize output_grid
    first_nonzero, seed_row = get_first_nonzero(input_grid)
    output_height = input_grid.shape[0]
    output_width = input_grid.shape[1]
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # change output pixels
    if first_nonzero != 0:
        triangle_height = seed_row + 1
        for i in range(triangle_height):
            for j in range(i + 1):
                output_grid[i, j] = first_nonzero

    return output_grid