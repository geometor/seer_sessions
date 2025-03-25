```python
"""
1.  **Initialization:** Start with an output grid identical to the input grid.

2.  **Identify Targets:** Locate all '5' (gray) pixels in the input grid.

3.  **Conditional Replacement - Phase 1:** For each '5' pixel:

    *   If any of its adjacent cells (horizontal, vertical, or diagonal) are '7' (orange), try to change that '7' to '8' (azure) in a specific manner explained below.
4.  **Conditional Replacement - Phase 2:**
    *   Iterate through every '7' cell.
    *   If a '7' cell is adjacent to any '5', change the original '7' cell to '8'.
    *   Prioritize adjacent 7s using this order Top, Bottom, Left, Right, Diagonals.
5. **Preservation:** All cells that are *not* '7' (orange) and adjacent to a '5' remain unchanged.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Returns a list of neighbors for a given cell, including diagonals.
    """
    rows, cols = len(grid), len(grid[0])
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append((i, j))
    return neighbors

def transform(input_grid):
    # initialize output_grid as a copy of input_grid
    output_grid = [row[:] for row in input_grid]
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Iterate through each cell in the grid
    for row in range(rows):
      for col in range(cols):
        #check current cell if it is 7
        if input_grid[row][col] == 7:
          # get neighbors of 7
          neighbors = get_neighbors(input_grid,row,col)
          #check neighbors if they are 5, if yes change original 7 cell to 8
          for neighbor_row,neighbor_col in neighbors:
            if input_grid[neighbor_row][neighbor_col] == 5:
              output_grid[row][col] = 8
              break #only replace at the first instance of 5

    return output_grid
```