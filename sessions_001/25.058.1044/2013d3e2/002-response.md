# 2013d3e2 • 002 • example_2 • investigate_coder

---
```python
"""
Extracts a reduced 3x3 section from the center of a 10x10 input grid, focusing on the non-zero colored pixels.
"""

import numpy as np

def find_first_non_zero_row(grid):
    """Finds the index of the first row that is not all zeros, scanning from top down"""
    for i, row in enumerate(grid):
        if not np.all(row == 0):
            return i
    return 0

def find_first_non_zero_col(grid):
    """Find the index of the first column that is not all zeros, scanning from left to right"""
    for i in range(grid.shape[1]):
        if not np.all(grid[:, i] == 0):
            return i
    return 0

def transform(input_grid):
    """
    Transforms the input grid by extracting a 3x3 region around the center and reducing
    empty rows.

    Args:
        input_grid (list of lists): A 10x10 grid represented as a list of lists.

    Returns:
        list of lists: The reduced 3x3 subgrid.
    """
    # Convert input_grid to numpy array for easier manipulation
    grid = np.array(input_grid)

    # Find the starting row and col of content
    row_start = find_first_non_zero_row(grid)
    col_start = find_first_non_zero_col(grid)

    # Extract the 3x3 subgrid
    subgrid = grid[row_start:row_start+3, col_start:col_start+3]

    return subgrid.tolist()
```
