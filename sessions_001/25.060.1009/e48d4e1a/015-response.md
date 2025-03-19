# e48d4e1a • 015 • refine_coder

---
```python
"""
The transformation identifies a yellow 'cross' shaped object.
The vertical component of the cross is moved to the leftmost column of the output grid.
The horizontal component of the cross is moved to row index 6, replacing existing objects,
and expanding to include every column in that row.
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
        for r, _ in vertical_bar:
            output_grid[r, 0] = 4

    # move horizontal bar to row index 6 and expand
    if horizontal_bar:
          new_row = 6
          if 0 <= new_row < rows:
            for c in range(cols):
              output_grid[new_row,c] = 4


    return output_grid
```
