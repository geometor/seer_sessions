# f25ffba3 • 002 • example_2 • investigate_coder

---
```python
"""
The transformation rule involves identifying a "filled rectangle" in the bottom-right corner of the input grid and then performing a vertical flip of the entire grid. The bottom row of the input becomes the top row of the output, and the top row of the input becomes the bottom row.
"""

import numpy as np

def find_filled_rectangle(grid):
    """
    Locates the contiguous block of non-zero pixels in the bottom-right corner.
    For simplicity, we assume the "filled rectangle" always touches the bottom and right edges.
    """
    rows, cols = grid.shape
    bottom_row = rows - 1
    right_col = cols - 1

    # Find top boundary
    top_row = bottom_row
    while top_row >= 0 and grid[top_row, right_col] != 0:
        top_row -= 1
    top_row += 1

    # Find left boundary
    left_col = right_col
    while left_col >= 0 and grid[bottom_row, left_col] != 0:
        left_col -= 1
    left_col += 1

    return (top_row, left_col, bottom_row, right_col)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Vertical Flip (entire grid)
    for i in range(rows):
        output_grid[i, :] = input_grid[rows - 1 - i, :]
    
    # # Copy the bottom row of input to the top of output.  Not necessary - handled by flip
    # output_grid[0, :] = input_grid[rows-1, :]
    # # Copy the top row of input to bottom of output. Not necessary. - handled by flip
    # output_grid[rows-1,:] = input_grid[0,:]


    return output_grid
```
