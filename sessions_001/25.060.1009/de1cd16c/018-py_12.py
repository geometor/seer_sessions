"""
Identify the bottom rectangular region in the input grid and output its color value as a single-element grid.
"""

import numpy as np

def find_bottom_region_color(grid):
    # Find the last row index where any change occurs (start of the bottom region).
    rows, cols = grid.shape
    last_change_row = 0
    # Find the index where color from the border changes.
    for i in range(1,rows):
      if not np.array_equal(grid[i], grid[0]):
        last_change_row = i
        break

    if last_change_row != 0:
      return grid[last_change_row,0]
    else:
        return grid[0,0]

def transform(input_grid):
    """
    Identifies the bottom region and output its color value.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    grid = np.array(input_grid)

    # Find the color of the bottom region
    bottom_color = find_bottom_region_color(grid)

    # Create a 1x1 output grid with the identified color
    output_grid = np.array([[bottom_color]])

    return output_grid