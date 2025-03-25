"""
The input grid is mirrored along a horizontal axis placed immediately below the input grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height = len(input_grid)
    input_width = len(input_grid[0])
    output_height = 2 * input_height
    output_grid = np.zeros((output_height, input_width), dtype=int)

    # Copy Input: Copy the input grid to the top half of the output grid.
    for i in range(input_height):
        for j in range(input_width):
            output_grid[i, j] = input_grid[i][j]

    # Reflect: Copy each row of the original input, in reverse order of rows,
    # onto the bottom half of the output grid.
    for i in range(input_height):
        for j in range(input_width):
            output_grid[input_height + i, j] = input_grid[input_height - 1 - i][j]

    return output_grid