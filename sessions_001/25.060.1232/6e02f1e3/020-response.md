# 6e02f1e3 • 020 • refine_coder

---
```python
"""
1.  **Identify the Top Row:** Find the topmost row of the input grid.
2.  **Top Row Transformation:** Change the color of all pixels in the top row to gray.
3.  **Identify the Bottom Row:** Find the bottommost row of the input grid.
4. **Bottom Row Transformation:** Change the color of the pixels in the bottom row to white *if the row is not the top row*.
5.  **Identify Corners:** If the corners have one color, and the top row has that same color, change all corner colors to white, *if it is not already white*.
6.  **Other Rows:** Examine all the rows that are not the top or bottom.  If a pixel is not part of the top row or bottom row, and it does not have the same value of the bottom row, and it is at the edge, make the pixel the same color as the bottom row.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 1 & 2. Change the top row to gray (5)
    for j in range(cols):
        output_grid[0, j] = 5

    # 3 & 4. Change the bottom row to white (0) if it's not the top row
    if rows > 1:
        for j in range(cols):
            output_grid[rows - 1, j] = 0

    # 5. Change corners to white if they match the top row's original color
    if rows > 1 and cols > 1: # Ensure there are corners
      top_left_orig = input_grid[0,0]
      if input_grid[0,0] == top_left_orig:
          if output_grid[0,0] != 0:
            output_grid[0, 0] = 0
      if input_grid[0, cols-1] == top_left_orig:
          if output_grid[0, cols-1] != 0:
            output_grid[0, cols-1] = 0
      if input_grid[rows-1, 0] == top_left_orig:
          if output_grid[rows-1, 0] != 0:
            output_grid[rows - 1, 0] = 0
      if input_grid[rows-1, cols-1] == top_left_orig:
          if output_grid[rows-1, cols-1] !=0:
            output_grid[rows - 1, cols - 1] = 0


    # 6. Change edge pixels of other rows to white, if they match top color
    for i in range(1, rows - 1):
        if cols > 0:
            if output_grid[i,0] != 0 and input_grid[i,0] == input_grid[0,0]:
              output_grid[i, 0] = 0
            if output_grid[i, cols-1] != 0 and input_grid[i, cols -1] == input_grid[0,0]:
                output_grid[i, cols - 1] = 0


    return output_grid
```
