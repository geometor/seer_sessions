"""
The input grid is transformed by inverting rows and columns, then mirrored.
Each element at input[row][column] will map to output[width - column - 1][height - row - 1].
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # change output pixels 
    for r in range(height):
        for c in range(width):
            output_grid[width - c - 1][height - r - 1] = input_grid[r][c]

    return output_grid.tolist()