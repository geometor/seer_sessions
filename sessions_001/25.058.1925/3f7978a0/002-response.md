# 3f7978a0 • 002 • example_3 • investigate_coder

---
```python
"""
The transformation extracts the smallest rectangular subgrid from the input grid that encloses all non-zero pixels.
"""

import numpy as np

def find_boundary_indices(grid):
    # Find rows and columns with non-zero elements
    non_zero_rows = np.any(grid != 0, axis=1)
    non_zero_cols = np.any(grid != 0, axis=0)

    # Get indices of the first and last True values
    rows = np.where(non_zero_rows)[0]
    cols = np.where(non_zero_cols)[0]
    
    if rows.size == 0 or cols.size == 0:  # Handle empty grids
        return 0, 0, 0, 0

    top = rows[0]
    bottom = rows[-1]
    left = cols[0]
    right = cols[-1]

    return top, bottom, left, right

def transform(input_grid):
    """
    Extracts the smallest rectangular subgrid enclosing all non-zero pixels.
    """
    # Convert input grid to a NumPy array for easier manipulation
    grid = np.array(input_grid)

    # Find boundary indices
    top, bottom, left, right = find_boundary_indices(grid)

    # Extract the subgrid
    output_grid = grid[top:bottom+1, left:right+1]

    return output_grid.tolist()
```
