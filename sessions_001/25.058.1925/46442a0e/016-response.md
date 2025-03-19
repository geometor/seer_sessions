# 46442a0e • 016 • example_3 • investigate_coder

---
```python
"""
Expands a 2x2 core of an input grid to 4x4 and then mirrors/duplicates the input's rows and columns to create a 6x6 output grid.
"""

import numpy as np

def find_core(grid):
    # Find the 2x2 yellow (4) core in the input grid.  Assumes it exists and is unique.
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            if grid[r, c] == 4 and grid[r + 1, c] == 4 and grid[r, c + 1] == 4 and grid[r + 1, c + 1] == 4:
                return (r, c)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((6, 6), dtype=int)

    # Find the 2x2 core
    core_row, core_col = find_core(input_grid)

    # Expand Core: Place the 2x2 core into the center of the output grid, making it 4x4.
    output_grid[1:5, 1:5] = 4

    # Mirror/Duplicate Columns:
    #   - input_grid[:,0] becomes the 1th column
    #   - input_grid[:,0] becomes the last column
    output_grid[1:5,0] = input_grid[0: , 0]
    output_grid[1:5,5] = input_grid[0: , 0]

    # Mirror/Duplicate rows
    #   - copy extended last row of input grid, including new columns
    #      and duplicate it into the last row of output
    #   - mirror extended first row, including new columns and make it first row of output.

    output_grid[5, 1:5] = input_grid[2,:]
    output_grid[5,0] = input_grid[2,0]
    output_grid[5,5] = input_grid[2,0]

    output_grid[0, 1:5] = input_grid[0,:]
    output_grid[0,0] = input_grid[0,0]
    output_grid[0,5] = input_grid[0,0]

    return output_grid
```
