# 99b1bc43 • 010 • refine_coder

---
```python
"""
The input grid is transformed into a 4x4 output grid. The output grid represents
a condensed version of the input, highlighting the non-zero corners
of colored regions in each quadrant of the input grid with green(3).
"""

import numpy as np

def get_quadrant(input_grid, row_start, row_end, col_start, col_end):
    return input_grid[row_start:row_end, col_start:col_end]

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((4, 4), dtype=int)

    # Define quadrant boundaries
    row_mid = rows // 2
    col_mid = cols // 2

    # Quadrant 1 (Top-Left)
    quadrant1 = get_quadrant(input_grid, 0, row_mid, 0, col_mid)
    if quadrant1.size > 0 and np.any(quadrant1 != 0):
        output_grid[0, 0] = 3

    # Quadrant 2 (Top-Right)
    quadrant2 = get_quadrant(input_grid, 0, row_mid, col_mid, cols)
    if quadrant2.size > 0 and np.any(quadrant2 != 0):
        output_grid[0, 3] = 3

    # Quadrant 3 (Bottom-Left)
    quadrant3 = get_quadrant(input_grid, row_mid, rows, 0, col_mid)
    if quadrant3.size > 0 and np.any(quadrant3 != 0):
        output_grid[3, 0] = 3

    # Quadrant 4 (Bottom-Right)
    quadrant4 = get_quadrant(input_grid, row_mid, rows, col_mid, cols)
    if quadrant4.size > 0 and np.any(quadrant4 != 0):
        output_grid[3, 3] = 3
    
    return output_grid.tolist()
```

