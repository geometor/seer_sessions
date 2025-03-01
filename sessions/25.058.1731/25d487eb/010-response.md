# 25d487eb • 010 • refine_coder

---
```python
"""
1.  **Locate:** Find the single blue (1) pixel in the input grid.
2.  **Expand:** From the initial blue pixel location, expand the blue color (1) into adjacent white pixels (0), creating either a vertical or horizontal line.
3. **Expansion Direction:** Expansion occurs in one direction along a single axis, either horizontally or vertically (not diagonally).
4.  **Stopping Condition:** The expansion stops when either the edge of the grid is reached, or a non-white (non-0) pixel is encountered.
5. **Preservation:** All other pixels that are not subject to expansion remain unchanged.
"""

import numpy as np

def find_blue_pixel(grid):
    # find the coordinates of the blue pixel (value 1)
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
          if value == 1:
            return (r,c)
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # find the blue pixel
    blue_pixel_coords = find_blue_pixel(input_grid)

    if blue_pixel_coords:
      row, col = blue_pixel_coords

      # Expand upwards
      for r in range(row - 1, -1, -1):
          if output_grid[r, col] != 0:
              break
          output_grid[r, col] = 1

      # Expand downwards
      for r in range(row + 1, output_grid.shape[0]):
          if output_grid[r, col] != 0:
              break
          output_grid[r, col] = 1

      # Expand right
      for c in range(col + 1, output_grid.shape[1]):
          if output_grid[row, c] != 0:
              break
          output_grid[row, c] = 1

      # Expand left
      for c in range(col - 1, -1, -1):
          if output_grid[row, c] != 0:
              break
          output_grid[row, c] = 1


    return output_grid
```
