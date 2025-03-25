```python
"""
The function identifies a contiguous region of non-zero pixels in the input grid (the object),
transposes its dimensions, and then fills the new grid as if the object was rotated 90 degrees
counter-clockwise.
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
        return []  # Return empty grid if no object

    object_grid, _ = object_data
    object_rows, object_cols = object_grid.shape

    # 2. Transpose Dimensions
    output_rows, output_cols = object_cols, object_rows
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # 3. Rotate and Replicate (90 degrees counter-clockwise)
    for r in range(output_rows):
        for c in range(output_cols):
            output_grid[r, c] = object_grid[c, r]

    return output_grid.tolist()
```