# 6ecd11f4 • 002 • example_3 • investigate_coder

---
```python
"""
Extracts a rectangular, non-white subgrid from the bottom area of a larger input grid.
"""

import numpy as np

def find_non_white_rectangle(grid):
    """Finds the bounding box of the smallest rectangle of non-white pixels."""
    rows, cols = grid.shape
    min_row, min_col = rows, cols
    max_row, max_col = -1, -1

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                min_row = min(min_row, r)
                min_col = min(min_col, c)
                max_row = max(max_row, r)
                max_col = max(max_col, c)

    if max_row == -1:  # Handle the case where the grid is all white.
      return None, None, None, None
    return min_row, min_col, max_row + 1, max_col + 1

def transform(input_grid):
    """
    Extracts a rectangular region of non-white pixels from the input grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid)

    # Find the bounding box of the non-white rectangle
    min_row, min_col, max_row, max_col = find_non_white_rectangle(grid)
    
    if min_row is None: # if no rectangle is found, return empty grid.
        return []

    # Extract the subgrid using array slicing
    output_grid = grid[min_row:max_row, min_col:max_col].tolist()

    return output_grid
```
