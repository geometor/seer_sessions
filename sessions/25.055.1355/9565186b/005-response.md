# 9565186b • 005 • refine_coder

---
```python
"""
Transforms blue (1) and light blue (8) pixels to gray (5) based on their
neighbors, other colors remain unchanged.
"""

import numpy as np

def get_neighbors(grid, row, col):
    neighbors = {}
    rows, cols = grid.shape
    if row > 0:
        neighbors["up"] = int(grid[row-1, col])
    if row < rows - 1:
        neighbors["down"] = int(grid[row+1, col])
    if col > 0:
        neighbors["left"] = int(grid[row, col-1])
    if col < cols - 1:
        neighbors["right"] = int(grid[row, col+1])
    return neighbors

def count_adjacent_neighbors(neighbors):
    return len(neighbors)

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel of the grid
    for i in range(rows):
        for j in range(cols):
            # change output pixels based on color and neighbor rules
            if output_grid[i, j] == 1 or output_grid[i, j] == 8:
                neighbors = get_neighbors(input_grid, i, j)
                adjacent_count = count_adjacent_neighbors(neighbors)

                #top edge and surrounded on 3 sides
                if i == 0 and adjacent_count == 3:
                     output_grid[i,j] = 5

                #if neighbors exist on at least 2 adjecent sides
                if adjacent_count >= 2:
                    output_grid[i, j] = 5


    return output_grid
```
