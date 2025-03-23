"""
The input grid is rotated 90 degrees counter-clockwise.  To determine the position of a pixel in the output grid, take the pixel at position (x, y) in the input grid.  Its new position (x', y') in the output grid will be (input_grid_height - 1 - y, x). The values of the pixels remain unchanged during this transformation, only their positions are altered.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows = input_grid.shape[0]
    cols = input_grid.shape[1]
    output_grid = np.empty((cols, rows), dtype=int)

    # change output pixels 
    for x in range(rows):
        for y in range(cols):
            output_grid[cols - 1 - y, x] = input_grid[x, y]

    return output_grid.tolist()