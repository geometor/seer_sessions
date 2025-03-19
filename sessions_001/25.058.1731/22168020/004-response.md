# 22168020 • 004 • example_1 • investigate_coder

---
```python
"""
The transformation rule is to connect green pixels horizontally. Green pixels are
connected horizontally to form a single contiguous block and two green pixels at
the bottom.
"""

import numpy as np

def get_green_pixels(grid):
    """
    This method returns the positions of green pixels
    """
    green_pixels = []
    for row_idx, row in enumerate(grid):
        for col_idx, pixel in enumerate(row):
            if pixel == 3:
                green_pixels.append((row_idx, col_idx))
    return green_pixels

def transform(input_grid):
    """
    Connects green pixels horizontally in a grid.
    """
    output_grid = np.copy(input_grid)
    green_pixels = get_green_pixels(input_grid)

    # Connect the first two rows of green
    if len(green_pixels) > 0:
        min_col = min(p[1] for p in green_pixels if p[0] <= 1)
        max_col = max(p[1] for p in green_pixels if p[0] <= 1)
        for row in range(2):
          for col in range(min_col, max_col+1):
            output_grid[row, col] = 3

        #Connect third row
        min_col = min(p[1] for p in green_pixels if p[0] == 2)
        max_col = max(p[1] for p in green_pixels if p[0] == 2)

        for col in range(min_col, max_col+1):
          output_grid[2, col] = 3

    # Connect the bottom two rows of green
    if len(green_pixels) > 0:
        min_col = min(p[1] for p in green_pixels if p[0] > 2)
        max_col = max(p[1] for p in green_pixels if p[0] > 2)
        for row in range(3, 5):
          for col in range(min_col, max_col + 1):
              output_grid[row, col] = 3

    return output_grid
```
