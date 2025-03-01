# 93b581b8 • 012 • refine_coder

---
```python
"""
1.  **Identify the Blue Object:** Locate the blue pixel (value '1') in the input grid. This serves as the origin point.
2. **Move Origin:**  Move the blue pixel to output grid location (0, 0).
3.  **Translate Other Colors:** For each other color (red, yellow, magenta) present in the input grid:
    *   Calculate the row and column difference between blue pixel and each other color pixel.
    *  Apply this same difference to move the color from its original location to the new location, with (0,0) as the origin.
"""

import numpy as np

def find_object(grid, color):
    # Find the coordinates of a specific color in the grid.
    coords = np.argwhere(grid == color)
    return coords[0] if coords.size > 0 else None

def transform(input_grid):
    # Initialize output grid as a copy of the input grid, ensures same dimensions.
    output_grid = np.zeros_like(input_grid)

    # Find the blue pixel (value 1), the origin
    blue_coords_in = find_object(input_grid, 1)

    if blue_coords_in is None:
        return output_grid # No blue pixel, return original

    # place origin at 0,0
    output_grid[0,0] = 1

    # Find other colored pixels and translate them.
    for color in [2, 4, 6]:  # Red, Yellow, Magenta
      color_coords_in = find_object(input_grid, color)

      if color_coords_in is not None:
          # calculate relative position
          row_diff = color_coords_in[0] - blue_coords_in[0]
          col_diff = color_coords_in[1] - blue_coords_in[1]

          # new position based on translation
          new_row = row_diff
          new_col = col_diff
          output_grid[new_row, new_col] = color

    return output_grid
```
