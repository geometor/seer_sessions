```python
"""
The function identifies a contiguous region of non-zero pixels in the input grid (the object),
rotates it 90 degrees counter-clockwise, and produces a new grid representing this rotated object.
"""

import numpy as np

def find_object(grid):
    """Finds the bounding box of the largest contiguous non-zero region."""
    rows, cols = np.nonzero(grid)
    if len(rows) == 0:
        return None  # No object found
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)

    object_grid = grid[min_row:max_row+1, min_col:max_col+1]
    return object_grid, (min_row, min_col)

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    input_grid = np.array(input_grid)

    # 1. Identify the Object
    object_data = find_object(input_grid)
    if object_data is None:
        return []  # Return empty list if no object

    object_grid, _ = object_data
    object_rows, object_cols = object_grid.shape

    # 2. Determine Output Dimensions (Transpose)
    output_rows, output_cols = object_cols, object_rows
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # 3. Rotate 90 Degrees Counter-Clockwise and Replicate
    for r in range(object_rows):
        for c in range(object_cols):
            new_r = c
            new_c = object_rows - 1 - r
            output_grid[new_r, new_c] = object_grid[r, c]

    return output_grid.tolist()
```