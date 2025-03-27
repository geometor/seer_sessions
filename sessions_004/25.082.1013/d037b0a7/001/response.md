```python
"""
1.  **Identify the starting point:** Find all values in the right-most column.
2.  **Horizontal Propagation:** For each starting cell, copy the cell's value to all the cells to the left of it in the same row *up until* another non-zero is encountered.
3.  **Vertical propagation**: For the last row and right-most cell, fill upwards and leftwards respectively (until the first non-zero pixel)
4.  **Downward Propagation:** Starting from the top row and down, and left to right in each row, propagate each non-zero pixel directly down to the bottom of the grid.
"""

import numpy as np

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Horizontal Propagation from the right-most column
    for r in range(rows):
        for c in range(cols - 1, -1, -1):
            if input_grid[r, c] != 0:
                for k in range(c - 1, -1, -1):
                    if output_grid[r,k] == 0:
                        output_grid[r, k] = input_grid[r, c]
                    else:
                         break

    # Downward Propagation
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                for k in range(r + 1, rows):
                    output_grid[k, c] = output_grid[r,c]

    return output_grid
```