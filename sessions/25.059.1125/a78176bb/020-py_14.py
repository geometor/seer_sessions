"""
1. Identify the color and position of the single non-zero pixel in the input grid.
2. Create diagonals of this color in the output grid. The diagonals repeat across the entire grid, with the initial identified pixel serving as the starting point of one such diagonal.
"""

import numpy as np

def get_initial_pixel(grid):
    # find the x, y, and color of the non-zero pixel
    grid = np.array(grid)
    non_zero_indices = np.nonzero(grid)
    if len(non_zero_indices[0]) > 0:
        row = non_zero_indices[0][0]
        col = non_zero_indices[1][0]
        color = grid[row, col]
        return row, col, color
    return None, None, None

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    
    # Get the initial pixel information.
    row, col, color = get_initial_pixel(input_grid)

    # If no non-zero pixel is found, return a zero-filled grid.
    if color is None:
        return output_grid

    # Create the diagonal pattern.
    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            if (r - c) == (row - col):  # Same diagonal
              output_grid[r,c] = color
            elif (r-c - (row-col))%min(rows,cols) == 0:  # r-c == const
              output_grid[r,c] = color
            elif (r-c - (row-col))%-min(rows,cols) == 0: # r-c == const
              output_grid[r,c] = color


    return output_grid