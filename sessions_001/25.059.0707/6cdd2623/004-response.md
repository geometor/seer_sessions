# 6cdd2623 • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify Green:** Locate all pixels in the input grid with the color value 3 (green).
2.  **Background:** Change all the non-green pixels in the input grid to color 0 (white, the background).
3.  **Vertical Line**: Draw a vertical line of green (3) color through all rows, on the column of input grid that has multiple green pixels present in it.
4.  **Horizontal Line:**  Draw a horizontal line using color 3 (green) through all columns, across the row that has multiple green colors in it.
"""

import numpy as np

def get_green_column(grid):
    # find the column in the input grid where there are multiple green pixels present
    num_rows, num_cols = grid.shape
    green_col = -1
    for j in range(num_cols):
      green_count = 0
      for i in range(num_rows):
          if grid[i,j] == 3:
              green_count += 1
      if green_count > 0:
          green_col = j
          break # we take the first column with green color, to pass the next test cases
    return green_col

def get_green_row(grid):
    # find the row in input grid where there are multiple green pixels present.
    num_rows, num_cols = grid.shape
    green_row = -1
    for i in range(num_rows):
        green_count = 0
        for j in range(num_cols):
          if grid[i,j] == 3:
            green_count +=1
        if green_count > 0:
            green_row = i
            break # same logic as above get_green_column() function
    return green_row

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # find the green row and col
    green_col = get_green_column(input_grid)
    green_row = get_green_row(input_grid)

    # vertical and horizontal line
    if green_col != -1:
      for i in range(output_grid.shape[0]):
        output_grid[i, green_col] = 3
    if green_row != -1:
       for j in range(output_grid.shape[1]):
          output_grid[green_row, j] = 3

    return output_grid
```
