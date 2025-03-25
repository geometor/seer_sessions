```python
"""
The program uses the red (2) pixels in the lower half of the input grid as markers for removal, 
and the red (2) pixels in the upper half as a template to "paint" adjacent blue pixels red 
in the output grid. Blue pixels not adjacent to these upper-half red pixels are kept.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Gets the 8 neighbors of a cell (including diagonals).
    """
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append((i, j))
    return neighbors

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    mid_row = rows // 2

    # 1. Remove red pixels in the lower half.
    for r in range(mid_row, rows):
        for c in range(cols):
            if input_grid[r, c] == 2:
                output_grid[r, c] = 0

    # 2. Find red pixels in top half.
    top_red_pixels = []
    for r in range(0, mid_row):
        for c in range(cols):
            if input_grid[r,c] == 2:
                top_red_pixels.append((r,c))

    # 3 & 4. Propagate red to adjacent blue pixels.
    for r, c in top_red_pixels:
        neighbors = get_neighbors(input_grid, r, c)
        for nr, nc in neighbors:
            if input_grid[nr, nc] == 1:
                output_grid[nr, nc] = 2

    return output_grid
```