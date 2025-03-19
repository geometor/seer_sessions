"""
The input grid is rotated 90 degrees counter-clockwise to produce the output grid. Each pixel in the input grid maintains its color, but its position is changed according to the rotation. Specifically, a pixel at position (row, column) in the input grid will be at position (column, height - 1 - row) in the output grid, where height is the number of rows of input grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    output_grid = np.zeros((width, height), dtype=int)

    # change output pixels 
    for row in range(height):
        for col in range(width):
            output_grid[col, height - 1 - row] = input_grid[row, col]

    return output_grid.tolist()