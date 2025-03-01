"""
The input grid is transformed into the output grid by expanding each non-zero pixel into a rectangle that extends to the right edge of the grid and downwards until it hits either another rectangle or the edge of the grid.
"""

import numpy as np

def get_non_zero_pixels(grid):
    """Finds the positions of non-zero pixels in the grid."""
    return np.argwhere(grid != 0)

def expand_pixel(grid, start_row, start_col, color):
    """Expands a pixel to a rectangle to the right and down."""
    # go to right edge
    for col in range(start_col, grid.shape[1]):
        grid[start_row, col] = color

    # check downwards
    row = start_row + 1
    while row < grid.shape[0]:
        if all(grid[row, start_col:] == 0):
          for col in range(start_col, grid.shape[1]):
              grid[row, col] = color
          row += 1
        else:
          break



def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.zeros_like(input_grid)
    non_zero_pixels = get_non_zero_pixels(input_grid)

    for row, col in non_zero_pixels:
        color = input_grid[row, col]
        expand_pixel(output_grid, row, col, color)
    
    return output_grid