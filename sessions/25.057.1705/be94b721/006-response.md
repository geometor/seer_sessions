# be94b721 • 006 • refine_coder

---
```python
"""
Identify the contiguous region of blue pixels (color value 1) within the input grid.
Extract this region as the output grid. If there are no blue pixels return an empty grid.
"""

import numpy as np

def find_object(grid, color_value):
    """
    Finds the bounding box of a contiguous region of a specific color.
    """
    rows, cols = np.where(grid == color_value)
    if len(rows) == 0:
        return None  # Object not found
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    """
    Transforms the input grid by extracting the blue region.
    """
    # Find the bounding box of the blue region (color value 1).
    blue_bounding_box = find_object(input_grid, 1)

    if blue_bounding_box is None:
        return np.zeros((0, 0), dtype=int) #return empty grid if no object

    # Extract the blue region using the bounding box.
    (min_row, min_col), (max_row, max_col) = blue_bounding_box
    output_grid = input_grid[min_row:max_row+1, min_col:max_col+1]

    return output_grid
```
