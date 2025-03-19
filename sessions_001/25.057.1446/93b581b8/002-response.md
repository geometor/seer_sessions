# 93b581b8 • 002 • example_1 • investigate_coder

---
```python
"""
The transformation involves preserving a central 2x2 block of colored pixels and mirroring its edges outwards. Specifically:
1. Identify the 2x2 central block.
2. Mirror the last column of the 2x2 block upwards.
3. Mirror the first column of the 2x2 block downwards.
4. Mirror the last row of the 2x2 block rightwards.
5. Mirror the first row of the 2x2 block leftwards.
"""

import numpy as np

def find_central_block(grid):
    """Finds the 2x2 central block of non-zero pixels."""
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            block = grid[r:r+2, c:c+2]
            if np.all(block != 0):
                return r, c
    return None, None

def transform(input_grid):
    """Transforms the input grid according to the mirroring rules."""
    input_grid = np.array(input_grid)  # Ensure input is a numpy array
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify the 2x2 central block.
    start_row, start_col = find_central_block(input_grid)

    if start_row is None or start_col is None:
        return output_grid # returns the input if there is no central block

    central_block = input_grid[start_row:start_row+2, start_col:start_col+2]

    # 2. Mirror the last column upwards.
    output_grid[0:start_row, start_col+1:start_col+3] = central_block[0:start_row, 1][::-1, np.newaxis]
    output_grid[0:start_row, start_col+1:start_col+3] = np.tile(central_block[:, 1].reshape(2,1),(1,2))[0:start_row,:]


    # 3. Mirror the first column downwards.
    output_grid[start_row+2:, start_col-1:start_col+1] = central_block[0:, 0][:, np.newaxis]
    output_grid[start_row+2:, start_col:start_col+2] =  np.tile(central_block[:, 0].reshape(2,1),(1,2))


    # 4. Mirror the bottom row right.
    output_grid[start_row:start_row+2, start_col+2:] =  np.tile(central_block[1, :],(1,2))[:,:2]

    #5. Mirror the top row left.

    output_grid[start_row:start_row+2, 0:start_col] = np.tile(central_block[0, :],(1,2))[:,:2][:,::-1]

    return output_grid
```
