# a699fb00 • 004 • example_1 • investigate_coder

---
```python
"""
Iterate through the input grid. Identify blue pixels (value 1). For each blue pixel, check its four directly adjacent neighbors. 
If a blue pixel has exactly two blue neighbors, change it to red (value 2). All other pixels remain unchanged.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
        gets the neighbors of grid[row,col] using cardinal directions, not diagonal
        returns: list of neighbor values
    """
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append(grid[row-1, col])  # Up
    if row < rows - 1:
        neighbors.append(grid[row+1, col])  # Down
    if col > 0:
        neighbors.append(grid[row, col-1])  # Left
    if col < cols - 1:
        neighbors.append(grid[row, col+1])  # Right
    return neighbors

def transform(input_grid):
    # initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # iterate over each pixel in the grid
    for row in range(rows):
        for col in range(cols):
            # check if the current pixel is blue (1)
            if input_grid[row, col] == 1:
                # get the values of the four neighbors
                neighbors = get_neighbors(input_grid, row, col)
                # count how many neighbors are blue (1)
                blue_neighbors_count = neighbors.count(1)
                # if exactly two neighbors are blue, change pixel to red (2)
                if blue_neighbors_count == 2:
                    output_grid[row, col] = 2

    return output_grid
```
