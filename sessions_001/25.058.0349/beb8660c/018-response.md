# beb8660c • 018 • refine_coder

---
```python
"""
1.  Identify the top-left 2x2 subgrid within the input grid.
2.  Rotate this 2x2 subgrid 90 degrees clockwise. Specifically:
    *   The value at position (0, 0) moves to (1, 0).
    *   The value at position (1, 0) moves to (1, 1).
    *   The value at position (1, 1) moves to (0, 1).
    *   The value at position (0, 1) moves to (0, 0).
3. Preserve all rows from the original that are located at row index 2 or greater.
4.  Output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # get dimensions of the input grid
    rows = output_grid.shape[0]
    cols = output_grid.shape[1]

    # rotate the top-left 2x2 subgrid clockwise by 90 degrees
    # only if grid has at least 2 rows and 2 cols.
    if rows >= 2 and cols >= 2:
        # cell(0,0) moves to cell(1,0)
        output_grid[1][0] = input_grid[0][0]
        # cell(1,0) moves to cell(1,1)
        output_grid[1][1] = input_grid[1][0]
        # cell(1,1) moves to cell (0,1)
        output_grid[0][1] = input_grid[1][1]
        # cell(0,1) moves to cell(0,0)
        output_grid[0][0] = input_grid[0][1]

    return output_grid
```

