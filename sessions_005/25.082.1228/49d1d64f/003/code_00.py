"""
Expands the input grid by duplicating each element horizontally and vertically, and adds a border of '0's at the top and left of the expanded grid.
"""

import numpy as np

def transform(input_grid):
    # Determine Input Dimensions
    input_rows = len(input_grid)
    input_cols = len(input_grid[0])

    # Create Output Grid
    output_rows = input_rows * 2
    output_cols = input_cols * 2
    output_grid = np.zeros((output_rows + 1, output_cols + 1), dtype=int)


    # Expand and Duplicate Input
    for i in range(input_rows):
        for j in range(input_cols):
            # Copy the element's value to the output grid, shifted by 1 to account for border
            output_grid[i * 2 + 1][j * 2 + 1] = input_grid[i][j]
            output_grid[i * 2 + 1][j * 2 + 2] = input_grid[i][j]
            output_grid[i * 2 + 2][j * 2 + 1] = input_grid[i][j]
            output_grid[i * 2 + 2][j * 2 + 2] = input_grid[i][j]

    # Add top border
    for j in range(input_cols):
        output_grid[0][j*2+1] = output_grid[1][j*2+1]
        output_grid[0][j*2+2] = output_grid[1][j*2+2]

      # Add bottom border
    for j in range(input_cols):
        output_grid[output_rows][j*2+1] = output_grid[output_rows-1][j*2+1]
        output_grid[output_rows][j*2+2] = output_grid[output_rows-1][j*2+2]
    return output_grid