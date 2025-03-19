"""
The colored pixel moves diagonally up and to the left by one position, and its color changes from red to green. All other pixels remain white.
"""

import numpy as np

def find_colored_pixel(grid):
    # Find the coordinates of the non-zero pixel.
    rows, cols = np.where(grid != 0)
    if len(rows) > 0:  # Ensure a non-zero pixel was found
      return rows[0], cols[0]
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find the colored pixel in the input grid.
    colored_pixel_coords = find_colored_pixel(input_grid)

    if colored_pixel_coords:
      # change output pixels
      row, col = colored_pixel_coords
      new_row = row - 1
      new_col = col - 1
      output_grid[new_row, new_col] = 3


    return output_grid