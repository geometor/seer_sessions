# 7447852a • 008 • example_1 • investigate_coder

---
```python
"""
Transforms an input grid by changing certain red pixels to yellow based on their position relative to white pixels and then propagating the yellow color to the row below.
"""

import numpy as np

def get_red_pixels(grid):
    # use where to find red pixels
    red_pixels = np.where(grid == 2)
    # combine and return list of (row, col)
    return list(zip(red_pixels[0], red_pixels[1]))

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    red_pixels = get_red_pixels(input_grid)
    
    # create dictionary, keys are row, values are column
    red_pixels_by_row = {}
    for r, c in red_pixels:
        if r not in red_pixels_by_row:
            red_pixels_by_row[r] = []
        red_pixels_by_row[r].append(c)

    # sort red pixels by column
    for row in red_pixels_by_row:
      red_pixels_by_row[row].sort()

    for row in red_pixels_by_row:
      col_indices = red_pixels_by_row[row]
      for i in range(len(col_indices)):
          current_col = col_indices[i]
          # check if all next are 0 until next 2 or end
          next_red_index = -1
          all_white = True
          for j in range(current_col + 1, cols):
            if output_grid[row, j] == 2:
              next_red_index = j
              break;
            elif output_grid[row,j] != 0:
              all_white = False
              break
          
          if all_white and next_red_index != -1:
            output_grid[row, next_red_index] = 4

    # propagate yellow color down
    for r in range(rows - 1):
        for c in range(cols):
            if output_grid[r, c] == 4:
                output_grid[r + 1, c] = 4

    return output_grid
```
