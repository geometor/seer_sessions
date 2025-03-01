# dc1df850 • 004 • example_1 • investigate_coder

---
```python
"""
Preserve non-white pixels (red and magenta) from the input to the output grid. Define a region bounded by the rightmost red pixel's column, the row above the magenta pixel, and the edges of the grid. Fill this region with blue pixels. Leave other white pixels unchanged.
"""

import numpy as np

def find_rightmost_red(grid):
    red_pixels = np.argwhere(grid == 2)
    if len(red_pixels) == 0:
      return None
    
    rightmost_red_column = np.max(red_pixels[:, 1])
    return rightmost_red_column

def find_magenta_row(grid):
  magenta_pixels = np.argwhere(grid == 6)
  if len(magenta_pixels) == 0:
    return None
  return magenta_pixels[0][0]

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find boundaries
    magenta_row = find_magenta_row(input_grid)
    rightmost_red_col = find_rightmost_red(input_grid)
    
    if rightmost_red_col is None:
      rightmost_red_col = cols
      
    if magenta_row is None:
       return output_grid

    # Fill with blue
    for r in range(rows):
        for c in range(cols):
            if output_grid[r,c] == 0 and r < magenta_row and c <= rightmost_red_col:
                output_grid[r, c] = 1

    return output_grid
```
