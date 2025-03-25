```python
"""
1. Downward Propagation: For each cell in the grid, if the cell directly *below* it has a value of 0, then the cell below takes the value of the current cell. This is done row by row.
2. Rightward Propagation: For each cell in the grid, if the cell *to the right* has a value of 0, then the cell to the right takes the value of the current cell. This is done for all columns.
"""

import numpy as np

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Downward Propagation
    for r in range(rows - 1):  # Iterate up to the second-to-last row
        for c in range(cols):
            if output_grid[r + 1, c] == 0:  # Check if the cell below is 0
                output_grid[r + 1, c] = output_grid[r, c]  # Propagate value down

    # Rightward Propagation
    for r in range(rows):
        for c in range(cols - 1):  # Iterate up to the second-to-last column
            if output_grid[r, c + 1] == 0:  # Check if the cell to the right is 0
                output_grid[r, c + 1] = output_grid[r, c]  # Propagate value right

    return output_grid
```
