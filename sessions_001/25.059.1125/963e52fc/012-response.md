# 963e52fc • 012 • refine_coder

---
```python
"""
The transformation rule involves identifying the non-white pixels in the input grid and duplicating them horizontally.
If the non-white pixels form a contiguous horizontal line, the line is duplicated.
If the non-white pixels form a shape, the shape is duplicated.
"""

import numpy as np

def find_non_white_pixels(grid):
    """Finds the coordinates and colors of non-white pixels."""
    rows, cols = grid.shape
    non_white_pixels = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                non_white_pixels.append(((r, c), grid[r, c]))
    return non_white_pixels

def transform(input_grid):
    # initialize output_grid: double the width, keep height the same
    output_grid = np.zeros((input_grid.shape[0], input_grid.shape[1] * 2), dtype=int)

    # Find non-white pixels
    non_white_pixels = find_non_white_pixels(input_grid)

    # Duplicate the non-white pixels
    for (row, col), color in non_white_pixels:
      output_grid[row, col] = color
      output_grid[row, col + input_grid.shape[1]] = color


    return output_grid
```

