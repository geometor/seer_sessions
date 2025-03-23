"""
The transformation is a reflection across the main anti-diagonal, which means to swap element from index `grid[row][col]` with element `grid[width-col-1][height-row-1]`.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # change output pixels
    for row in range(height):
        for col in range(width):
            output_grid[width-col-1][height-row-1] = input_grid[row][col]

    return output_grid.tolist()