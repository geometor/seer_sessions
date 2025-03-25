```python
"""
Shifts non-bottom-row yellow pixels in each column downwards by one row, extending the yellow to fill the spaces above, while preserving the bottom row of yellow pixels.
"""

import numpy as np

def get_yellow_pixels(grid):
    """
    Finds coordinates of all yellow pixels in the grid.
    """
    yellow_pixels = []
    for row_idx, row in enumerate(grid):
        for col_idx, pixel in enumerate(row):
            if pixel == 4:
                yellow_pixels.append((row_idx, col_idx))
    return yellow_pixels

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Get all yellow pixel coordinates
    yellow_pixels = get_yellow_pixels(input_grid)

    # Iterate through columns
    for col in range(cols):
        # Get yellow pixel row indices in the current column (excluding the bottom row)
        yellow_rows = [row for row, c in yellow_pixels if c == col and row != rows - 1]

        # If there are yellow pixels in the column (excluding bottom row)
        if yellow_rows:
          # find the lowest yellow pixel
          lowest_yellow = max(yellow_rows)

          # shift that down by one
          new_lowest = lowest_yellow + 1
            
          # set previous yellow blocks to 0 and the new one to 4
          # output_grid[lowest_yellow,col] = 0  # no clearing required - it will extend
          if new_lowest < rows -1:  # make sure its not the bottom row
            output_grid[new_lowest, col] = 4

            # fill above up to including prior location with yellow
            for r in range(0, new_lowest):
              output_grid[r,col] = 4
          else:
            # special case when lowest yellow is row above bottom
            for r in range(0, new_lowest):
              output_grid[r,col] = 4
    return output_grid.tolist()
```