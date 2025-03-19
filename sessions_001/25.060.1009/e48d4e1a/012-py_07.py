"""
The transformation rule is as follows:
1. Identify the cross shape formed by yellow (4) pixels in the input grid.
2. Move the vertical bar of the cross to the first column (index 0) of the output grid.
3. Move the horizontal bar of the cross to row 6 (index 6, which equals to original horizontal index +3) of the output grid, while maintaining its length.
4. Ignore other colors in the grid.
"""

import numpy as np

def get_cross_object(grid, color=4):
    rows, cols = grid.shape
    vertical_bar = []
    horizontal_bar = []

    # Find vertical bar
    for c in range(cols):
      for r in range(rows):
        if grid[r,c] == color:
          vertical_bar.append((r,c))
          break

    # Find the vertical bar's column
    vertical_col = -1
    if vertical_bar:
      vertical_col = vertical_bar[0][1]


    # Find Horizontal Bar
    for r in range(rows):
      for c in range(cols):
        if grid[r,c] == color:
            horizontal_bar.append((r,c))
            break

    # Find the horizontal bar's row
    horizontal_row = -1
    if horizontal_bar:
      horizontal_row = horizontal_bar[0][0]
        

    return vertical_bar, horizontal_bar, vertical_col, horizontal_row

def transform(input_grid):
    # Initialize output grid with zeros (white)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Get the cross object parts
    vertical_bar, horizontal_bar, vertical_col, horizontal_row = get_cross_object(input_grid)

    # Move the vertical bar to the first column
    if vertical_bar:
        for r in range(rows):
            output_grid[r, 0] = 4

    # move horizontal bar to row index 6
    if horizontal_bar:
          new_row = horizontal_row + 3
          if 0 <= new_row < rows:
            for c in range(cols):
              output_grid[new_row,c] = 4


    return output_grid