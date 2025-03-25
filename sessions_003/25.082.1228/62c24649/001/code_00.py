"""
The input grid is doubled in both the x and y dimensions. The output grid's dimensions are twice the size of the input grid. The content of the input grid is replicated in a mirrored fashion to fill the output grid.
"""

import numpy as np

def transform(input_grid):
    # Get Dimensions of input
    h, w = input_grid.shape

    # Create Output Grid: (2h x 2w)
    output_grid = np.zeros((2 * h, 2 * w), dtype=int)

    # Double horizontally
    for y in range(h):
        for x in range(w):
            output_grid[y, x] = input_grid[y, x]
            output_grid[y, 2*w - 1 - x] = input_grid[y, x]

    # Double vertically
    for y in range(h):
        for x in range(2 * w):
            output_grid[2*h - 1 - y, x] = output_grid[y,x]

    return output_grid