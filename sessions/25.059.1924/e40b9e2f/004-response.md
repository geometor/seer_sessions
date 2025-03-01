# e40b9e2f • 004 • example_1 • investigate_coder

---
```python
"""
The shape in the input is rotated by swapping the position of the colors and reflecting through x, y axis.
"""

import numpy as np

def get_shape_bounds(grid):
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find the bounding box of the shape
    bounds = get_shape_bounds(input_grid)
    if bounds is None:
        return output_grid

    min_row, max_row, min_col, max_col = bounds
    shape = input_grid[min_row:max_row+1, min_col:max_col+1]
    
    # Create a copy for modification.
    rotated_shape = np.copy(shape)

    # Swap colors: 4 becomes 7, 7 becomes 4.
    rotated_shape[shape == 4] = 77  # Temporary value to avoid double-swapping
    rotated_shape[shape == 7] = 4
    rotated_shape[rotated_shape == 77] = 7

    # Reflect across the horizontal and vertical center lines.
    rotated_shape = np.flipud(np.fliplr(rotated_shape))

    # Place the transformed shape back into the output grid.
    output_grid[min_row:max_row+1, min_col:max_col+1] = rotated_shape
    
    return output_grid
```
