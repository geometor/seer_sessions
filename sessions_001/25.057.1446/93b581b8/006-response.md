# 93b581b8 • 006 • refine_coder

---
```python
"""
1. Identify the Bounding Box: Find the smallest rectangle (bounding box) that encloses all non-zero (colored) pixels in the input grid.
2. Central Region: Consider the non-zero pixels inside the bounding box as a "central region". This region can be of any shape and size. It may or not be 2x2.
3. Expansion by Propagation: From the edges of this identified central region, propagate the colors outward, filling the entire output grid, and expand it to the boundaries of the largest possible grid in any direction. The colors should be propagated as they are in the central region, preserving the relative color arrangement within the identified region, and extending the final rows/columns of the bounding box outward.
"""

import numpy as np

def get_nonzero_bbox(grid):
    """Finds the bounding box of non-zero elements in a grid."""
    rows, cols = grid.shape
    nonzero_rows = np.any(grid != 0, axis=1)
    nonzero_cols = np.any(grid != 0, axis=0)
    if not np.any(nonzero_rows) or not np.any(nonzero_cols):
        return None  # Empty grid
    min_row, max_row = np.where(nonzero_rows)[0][[0, -1]]
    min_col, max_col = np.where(nonzero_cols)[0][[0, -1]]
    return (min_row, min_col, max_row + 1, max_col + 1)

def transform(input_grid):
    input_grid = np.array(input_grid)
    # 1. Identify the Bounding Box
    bbox = get_nonzero_bbox(input_grid)

    if bbox is None:
        return np.zeros_like(input_grid)  # Return an empty grid if input is all zeros

    min_row, min_col, max_row, max_col = bbox

    # 2. Central Region (implicitly defined by the bounding box)
    central_region = input_grid[min_row:max_row, min_col:max_col]

    # 3. Expansion by Propagation
    output_grid = np.zeros_like(input_grid) # initialize with same size

    output_rows, output_cols = output_grid.shape

    # Propagate top edge
    output_grid[0:min_row, min_col:max_col] = np.tile(central_region[0, :],(min_row,1))

    # Propagate bottom edge
    output_grid[max_row:output_rows, min_col:max_col] = np.tile(central_region[-1, :],(output_rows-max_row,1))

    # Propagate left edge
    output_grid[:,0:min_col] = np.tile(output_grid[:,min_col].reshape(-1,1),(1,min_col))

    # Propagate right edge
    output_grid[:,max_col:output_cols] = np.tile(output_grid[:,max_col-1].reshape(-1,1),(1,output_cols-max_col))

    return output_grid
```
