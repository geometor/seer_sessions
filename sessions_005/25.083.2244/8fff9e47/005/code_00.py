"""
The output grid is a 2x2 repetition of a sub-grid. The sub-grid's dimensions
are calculated from the input grid's dimensions. The sub-grid is populated
by taking a "diagonal transpose with inflation" of the top-left quadrant of the
input grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize grids and dimensions
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape
    sub_grid_height = input_height + input_height // 2
    sub_grid_width = input_width + input_width // 2
    output_grid = np.zeros((sub_grid_height * 2, sub_grid_width * 2), dtype=int)
    sub_input_height = input_height // 2
    sub_input_width = input_width // 2
    sub_input = input_grid[:sub_input_height, :sub_input_width]
    sub_grid = np.zeros((sub_grid_height, sub_grid_width), dtype=int)


    # Populate the sub-grid
    for x in range(sub_grid_height):
        for y in range(sub_grid_width):
            sub_grid[x, y] = sub_input[x % sub_input_height, y % sub_input_width]


    # Replicate the sub-grid 2x2 times to create output
    output_grid[:sub_grid_height, :sub_grid_width] = sub_grid
    output_grid[sub_grid_height:, :sub_grid_width] = sub_grid
    output_grid[:sub_grid_height, sub_grid_width:] = sub_grid
    output_grid[sub_grid_height:, sub_grid_width:] = sub_grid

    return output_grid