"""
The transformation involves replacing the central vertical gray pixels
with blue ones, and adding red pixels in the bottom left, according to those
rules.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing the color of specific gray pixels to blue,
    and add a red pixel to the lower left of gray blocks.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Get the height and width of the grid
    height, width = input_grid.shape

    # Find the central column index
    center_col = width // 2

    # 1. Replace gray pixels in the central column with blue pixels.
    for row in range(height):
      if output_grid[row, center_col] == 5:
        output_grid[row, center_col] = 1 # blue

    # 2. add a red pixel to the bottom left.
    # Identify gray columns.
    gray_cols = []
    for col in range(width):
      for row in range(height):
        if input_grid[row, col] == 5:
          gray_cols.append(col)
          break # optimization: next col after we know it contains gray
    
    if len(gray_cols) > 0:
        leftmost_gray_col = gray_cols[0]
        # now find the *last* gray row in this column
        last_gray_row = -1
        for row in range(height):
            if input_grid[row,leftmost_gray_col] == 5:
                last_gray_row = row
        if last_gray_row > -1:
          output_grid[last_gray_row, leftmost_gray_col] = 2

    return output_grid