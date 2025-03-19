# 3c9b0459 • 006 • refine_coder

---
```python
"""
The transformation rule involves decomposing the input into constituent colored objects, creating a bounding box, and filling it with colors based on the original objects.
"""

import numpy as np

def get_bounding_box(grid):
    """
    Finds the smallest bounding box that encloses all non-white pixels.
    Returns (min_row, min_col, max_row, max_col)
    """
    rows, cols = len(grid), len(grid[0])
    min_row, min_col = rows, cols
    max_row, max_col = -1, -1

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0:  # Not white
                min_row = min(min_row, r)
                min_col = min(min_col, c)
                max_row = max(max_row, r)
                max_col = max(max_col, c)

    return min_row, min_col, max_row, max_col

def transform(input_grid):
    """
    Transforms the input grid by creating a bounding box around non-white
    pixels and filling it with colors from original grid.
    """
    # 1. Find the bounding box.
    min_row, min_col, max_row, max_col = get_bounding_box(input_grid)

    # 2. Initialize the output grid with black.  Use bounding box size.
    # If no non-white pixels, return a 1x1 white grid.
    if max_row == -1:  # all white input
       return [[0]]
        
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    output_grid = [[0] * width for _ in range(height)] # initialize to black


    # 3.  fill with colors
    for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                output_grid[r-min_row][c-min_col] = input_grid[r][c]


    return output_grid
```
