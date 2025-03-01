# 6e02f1e3 • 012 • refine_coder

---
```python
"""
Transforms a 3x3 input grid into a 3x3 output grid, where:
- Green (3) pixels in the top row become white (0), except the last one becomes gray (5).
- Yellow (4) pixels in the left column become white (0), except the last one becomes gray (5).
- Red (2) pixels in the last two rows become white (0), except those at the edges in the last row and at the top right become gray (5).
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same shape and data type as the input grid.
    output_grid = np.zeros_like(input_grid)

    # Find the indices of green pixels in the top row.
    green_indices = np.where((input_grid[0, :] == 3))
    if len(green_indices[0]) > 0:
        # Change all to white (0)
        output_grid[0, green_indices] = 0
        # Change the last one to gray (5)
        output_grid[0, green_indices[0][-1]] = 5

    # Find the indices of yellow pixels in the left column
    yellow_indices = np.where((input_grid[:, 0] == 4))
    if len(yellow_indices[0]) > 0:
        # Change all to white
        output_grid[yellow_indices, 0] = 0
        # Change the last one to gray
        output_grid[yellow_indices[0][-1], 0] = 5

    # Find indices of red pixels in the last two rows.
    red_indices = np.where((input_grid[1:3, :] == 2))
    if len(red_indices[0]) > 0 :
      # Change all to white
      output_grid[red_indices[0] + 1, red_indices[1]] = 0

      # bottom-left corner to gray
      if input_grid[2,0] == 2:
          output_grid[2,0] = 5

      # top-right to gray
      # find top right most red in the last two rows

      max_col = -1
      top_right_row = -1
      top_right_col = -1

      for i in range(len(red_indices[0])):
        row = red_indices[0][i] + 1
        col = red_indices[1][i]
        if col >= max_col:
          max_col = col
          top_right_row = row
          top_right_col = col
      if top_right_row != -1:
        output_grid[top_right_row,top_right_col] = 5


    return output_grid
```
