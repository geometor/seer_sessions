"""
Expands the input grid by duplicating each element horizontally and vertically, and adds a border of '0's around the expanded grid.
"""

import numpy as np

def transform(input_grid):
    # Determine Input Dimensions
    input_rows = len(input_grid)
    input_cols = len(input_grid[0])

    # Create Output Grid with space for expansion and border
    output_rows = input_rows * 2 + 2  # +2 for top and bottom border
    output_cols = input_cols * 2 + 2  # +2 for left and right border
    output_grid = np.zeros((output_rows, output_cols), dtype=int)


    # Expand and Duplicate Input, shifted by 1 for the border
    for i in range(input_rows):
        for j in range(input_cols):
            # Copy the element's value to the output grid, shifted by 1 to account for border
            output_grid[i * 2 + 1][j * 2 + 1] = input_grid[i][j]
            output_grid[i * 2 + 1][j * 2 + 2] = input_grid[i][j]
            output_grid[i * 2 + 2][j * 2 + 1] = input_grid[i][j]
            output_grid[i * 2 + 2][j * 2 + 2] = input_grid[i][j]

    return output_grid