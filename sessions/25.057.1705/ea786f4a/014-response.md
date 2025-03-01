# ea786f4a • 014 • example_3 • investigate_coder

---
```python
"""
Transforms a grid by expanding a single white pixel (0) into a cross shape, replacing green pixels (3) along the horizontal and vertical axes.
"""

import numpy as np

def find_center_pixel(grid):
    # Find the coordinates of the white pixel (value 0).
    rows, cols = np.where(grid == 0)
    if len(rows) > 0:  # Check if a white pixel was found
       return rows[0], cols[0]
    return None  # Or handle the case where no white pixel is present

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the center white pixel.
    center = find_center_pixel(input_grid)
    if center is None:
        return output_grid # if no center, do nothing
    center_row, center_col = center

    # Expand vertically.
    for r in range(rows):
        output_grid[r, center_col] = 0

    # Expand horizontally.
    for c in range(cols):
        output_grid[center_row, c] = 0

    return output_grid
```
