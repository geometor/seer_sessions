# 25d487eb • 006 • example_1 • investigate_coder

---
```python
"""
1.  **Identify:** Locate the single blue (1) pixel within the input grid.
2.  **Expand:** From the position of identified blue pixel, replace all the pixels in the row to its right with blue pixels up to the right edge of the grid.
3.  **Maintain:** Do not modify the grid or any other pixels, except by previous step.
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
      # expand blue to the right
      for c in range(col + 1, output_grid.shape[1]):
          output_grid[row, c] = 1

    return output_grid
```
