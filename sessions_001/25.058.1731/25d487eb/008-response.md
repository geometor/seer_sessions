# 25d487eb • 008 • refine_coder

---
```python
"""
1.  **Locate:** Find the single blue (1) pixel in the input grid.
2.  **Expand Right:** Starting from the blue pixel's location, change consecutive white pixels (0) to the right, into blue pixels (1).
3.  **Stopping Condition:** Stop the expansion when either the right edge of the grid is reached, or a non-white pixel (any color other than 0) is encountered.
4. **Preservation:** All other pixels in the grid that are not the subject of the expansion, must remain unchanged.
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
      # expand blue to the right with stopping condition
      for c in range(col + 1, output_grid.shape[1]):
          if output_grid[row, c] != 0:  # Check for non-white pixel
              break  # Stop expansion
          output_grid[row, c] = 1

    return output_grid
```

