# a740d043 • 005 • refine_coder

---
```python
"""
1. Identify the bounding box: Find the smallest rectangle within the input grid that encloses all non-zero pixels.  This is defined by the minimum and maximum row and column indices of the non-zero pixels.
2. Extract Subgrid: Extract the section of the input grid defined by the bounding box in step 1.
3. Output: The extracted subgrid is the output.
"""

import numpy as np

def get_bounding_box(grid):
    """Finds the bounding box of non-zero elements in a NumPy grid."""
    rows = np.any(grid != 0, axis=1)
    cols = np.any(grid != 0, axis=0)
    if not np.any(rows) or not np.any(cols):
        return (0, 0, 0, 0)  # Empty bounding box for all-zero grid
    min_row, max_row = np.where(rows)[0][[0, -1]]
    min_col, max_col = np.where(cols)[0][[0, -1]]
    return (min_row, max_row, min_col, max_col)

def transform(input_grid):
    """Extracts the bounding box of non-zero pixels from the input grid."""

    # Find the bounding box
    min_row, max_row, min_col, max_col = get_bounding_box(input_grid)

    # Extract the subgrid
    output_grid = input_grid[min_row:max_row+1, min_col:max_col+1]

    return output_grid
```
