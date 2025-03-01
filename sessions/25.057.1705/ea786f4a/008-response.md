# ea786f4a • 008 • example_2 • investigate_coder

---
```python
"""
The transformation creates a white cross (+) shape centered on the original white pixel, extending to the edges of the grid. The '0' replaces any '2' that is in the same row or column as any existing '0'.
"""

import numpy as np

def get_center_white_pixel(grid):
    # Find the coordinates of the white pixel (value 0)
    white_pixels = np.argwhere(grid == 0)
    if len(white_pixels) > 0:
      return white_pixels[0]
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find initial white pixel
    center_white = get_center_white_pixel(input_grid)

    if center_white is not None:
        center_row, center_col = center_white

        # Propagate white color in the center row and column
        for r in range(rows):
          for c in range(cols):
            if input_grid[r][c] == 2:
              if r == center_row or c == center_col:
                output_grid[r][c] = 0

    # Extend white color
    for r in range(rows):
      for c in range(cols):
          if input_grid[r][c] == 2:
            if r == 0 or r == rows -1 or c == 0 or c == cols - 1:
              output_grid[r][c] = 0
    return output_grid
```
