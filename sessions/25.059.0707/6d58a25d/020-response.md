# 6d58a25d • 020 • refine_coder

---
```python
"""
1. Change all yellow (4) pixels to green (3).
2. Identify columns that contain either yellow (4) or green (3) pixels in the input grid.
3. Within each identified column, find the minimum and maximum row indices that contain either yellow or green.
4. Fill the region between the minimum and maximum row indices (inclusive) in those columns with green (3).
"""

import numpy as np

def get_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color)

def get_bounding_rows(input_grid, columns):
    """
    Finds min and max rows that contain yellow or green for the given columns
    """
    bounding_rows = {}
    for col in columns:
      rows_in_col = []
      for r,c in get_pixels_by_color(input_grid, 4):
          if c == col:
              rows_in_col.append(r)

      for r,c in get_pixels_by_color(input_grid, 3):
        if c == col:
            rows_in_col.append(r)
      if len(rows_in_col)>0:
        bounding_rows[col] = (min(rows_in_col), max(rows_in_col))
    return bounding_rows
def transform(input_grid):
    """Transforms the input grid according to the specified rules."""
    output_grid = np.copy(input_grid)
    #change yellow to green
    for r,c in get_pixels_by_color(input_grid, 4):
        output_grid[r,c] = 3

    #find columns that have yellow or green
    yellow_cols = set(get_pixels_by_color(input_grid, 4)[:,1]) if get_pixels_by_color(input_grid, 4).size > 0 else set()
    green_cols = set(get_pixels_by_color(input_grid, 3)[:,1]) if get_pixels_by_color(input_grid, 3).size > 0 else set()

    target_cols = list(yellow_cols.union(green_cols))

    #find bounding rows for target columns
    bounding_rows = get_bounding_rows(input_grid, target_cols)

    #fill between bounds
    for col, (min_row, max_row) in bounding_rows.items():
      for row in range(min_row, max_row+1):
        output_grid[row, col] = 3

    return output_grid
```
