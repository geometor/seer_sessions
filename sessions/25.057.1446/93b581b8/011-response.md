# 93b581b8 • 011 • refine_coder

---
```python
"""
1.  **Identify the Origin:** Find the blue pixel (color 1) in the input grid. This pixel will be the origin (0, 0) of a new coordinate system. Place this pixel at index [0,0] of a new, blank grid.
2.  **Relative Coordinates:** For each other colored pixel (red, yellow, magenta), calculate its position *relative* to the blue pixel. This is done by subtracting the blue pixel's row and column indices from the other pixel's row and column indices (row_diff = color_row - blue_row, col_diff = color_col - blue_col).
3. **Mirror:**  Create a mirrored version, at [blue_row - row_diff, blue_column - col_diff]
4. **Quadrant:** Yellow and Magenta objects should also be placed using the quadrant rule.
5.  **Output:** The transformed grid is the output.
"""

import numpy as np

def find_object(grid, color):
    # Find the coordinates of a specific color in the grid.
    coords = np.argwhere(grid == color)
    return coords[0] if coords.size > 0 else None

def transform(input_grid):
    # Initialize output grid as a copy of the input grid, then make blank
    output_grid = np.zeros_like(input_grid)

    # Find the blue pixel (value 1), the origin
    blue_coords = find_object(input_grid, 1)

    if blue_coords is None:
        return output_grid # No blue pixel, return blank

    # place origin at 0,0
    output_grid[0,0] = 1

    # Find other colored pixels and mirror them.
    for color in [2, 4, 6]:  # Red, Yellow, Magenta
      color_coords = find_object(input_grid, color)

      if color_coords is not None:
          # calculate relative position
          row_diff = color_coords[0] - blue_coords[0]
          col_diff = color_coords[1] - blue_coords[1]

          # Handle mirroring.
          output_grid[blue_coords[0] - row_diff , blue_coords[1]- col_diff] = color

          # Handle quadrant creation for yellow and magenta
          if color in [4,6]:
            output_grid[blue_coords[0] + (row_diff * 2), blue_coords[1] + (col_diff * 2)] = color
            output_grid[blue_coords[0] - (row_diff * 2), blue_coords[1] - (col_diff * 2)] = color

    return output_grid
```
