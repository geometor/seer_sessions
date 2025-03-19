# 2013d3e2 • 002 • example_1 • investigate_coder

---
```python
"""
Extracts the central non-zero colored region from the input grid.
"""

import numpy as np

def get_core_region_bounds(grid):
    """
    Finds the min/max row and col indices of non-zero pixels.
    """
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:  # Handle empty grid case (all zeros)
        return None, None, None, None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Extracts the smallest subgrid containing all non-zero pixels.
    """
    # Convert input grid to a NumPy array for easier manipulation
    grid = np.array(input_grid)

    # 1. Identify the Core Region & Determine Boundaries:
    min_row, max_row, min_col, max_col = get_core_region_bounds(grid)
    
    # Handle the case where the input grid contains only zeros
    if min_row is None:
        return [[]] # Return an empty grid

    # 2. Extract Subgrid:
    output_grid = grid[min_row:max_row+1, min_col:max_col+1].tolist()

    return output_grid
```
