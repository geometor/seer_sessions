"""
Copies a grid, replacing a 3x1 white block in the top-left corner with blue,
a 4x2 block of white pixels in the center rows with red, and the bottom-right
white pixel with green.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Replace top-left 3x1 white block with blue (1)
    for i in range(min(3, rows)):  # Iterate through the first 3 rows or fewer if the grid is smaller
        if input_grid[i, 0] == 0:
          output_grid[i, 0] = 1

    # Replace a central 4x2 block of white pixels with red (2)
    for i in range(4, 6): # Check only center rows 5 and 6 (index starts at 0)
        if i < rows:
            for j in range(cols - 3):
                if all(input_grid[i, j:j+4] == 0):
                    output_grid[i, j:j+4] = 2

    # find last row with a zero
    last_row = -1
    for r_idx in reversed(range(rows)):
        if 0 in input_grid[r_idx,:]:
            last_row = r_idx
            break

    # find last column in last_row with a zero
    last_col = -1
    if last_row != -1:
      for c_idx in reversed(range(cols)):
          if input_grid[last_row,c_idx] == 0:
              last_col = c_idx
              break

    # Replace bottom-right white pixel with green (3)
    if last_col != -1:
        output_grid[last_row, last_col] = 3

    return output_grid