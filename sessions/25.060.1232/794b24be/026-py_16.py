"""
The transformation rule is as follows:
1. Identify the non-zero cell in the input grid.
2. Change its value to 2.
3. Move non-zero cell, to the top-left corner of the output grid (0,0)
4. Set all the other cells in the output grid to 0.
"""

import numpy as np

def find_non_zero_cell(grid):
    # Iterate through the grid to find the non-zero cell
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] != 0:
                return (i, j)
    return None

def transform(input_grid):
    # Initialize the output grid with zeros, same size as input
    output_grid = np.zeros_like(input_grid)

    # Find the non-zero cell in the input grid
    non_zero_cell = find_non_zero_cell(input_grid)

    # If a non-zero cell exists
    if non_zero_cell:
        # Change the value to 2 at the top-left corner (0,0)
        output_grid[0, 0] = 2

    return output_grid