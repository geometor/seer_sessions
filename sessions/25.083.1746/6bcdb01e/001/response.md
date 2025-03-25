```python
"""
Replace orange (7) pixels with green (3) pixels, but only for those original orange pixels that are directly beside a green pixel.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Gets the immediate horizontal and vertical neighbors of a cell.
    """
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append(grid[row-1, col])
    if row < rows - 1:
        neighbors.append(grid[row+1, col])
    if col > 0:
        neighbors.append(grid[row, col-1])
    if col < cols - 1:
        neighbors.append(grid[row, col+1])
    return neighbors

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # iterate through each cell of the input_grid
    for row in range(rows):
        for col in range(cols):
            # check if it's orange (7)
            if input_grid[row, col] == 7:
                # check neighbors
                neighbors = get_neighbors(input_grid, row, col)
                # If any neighbor is green (3), replace with green (3)
                if 3 in neighbors:
                    output_grid[row, col] = 3

    return output_grid
```
