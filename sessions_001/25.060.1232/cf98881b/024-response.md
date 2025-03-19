# cf98881b • 024 • refine_coder

---
```python
"""
Extracts a 4x4 subgrid from the input grid. The subgrid's upper-left corner
is determined by the left-most, top-most non-zero cell in the input grid.
"""

import numpy as np

def find_upper_left_corner(grid):
    """
    Finds the top-left corner of the smallest rectangle containing all non-zero cells.
    """
    grid = np.array(grid)
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                return (r, c)
    return None

def transform(input_grid):
    """
    Extracts a 4x4 subgrid.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Find the upper-left corner of the subgrid
    corner = find_upper_left_corner(input_grid)

    if corner is None:
        return [[]] # Return Empty grid.

    r_start, c_start = corner
    
    # Calculate subgrid boundaries.
    r_end = r_start + 4
    c_end = c_start + 4

    # Ensure we don't exceed the original grid boundaries.
    if r_end > rows or c_end > cols:
          return [[]]

    # Extract Subgrid
    output_grid = input_grid[r_start:r_end, c_start:c_end]
    
    return output_grid.tolist()
```
