"""
1. Iterate through each cell (pixel) in the input grid.

2. First Pass - Change 1s and 7s:
    *   For each cell, check if its color is blue (1) or orange (7).
    *   If it is, examine its immediate neighbors (up, down, left, right, and diagonals).
    *   If *any* of these neighbors have a *different* color value AND the neighboring color is not azure (8), change the current cell's color to gray (5).
    *   Keep track of the cells changed to 5.

3. Second Pass - Change 8s:
    *   Iterate through each cell again
    *   If the current cell is an 8.
    *   If a neighboring cell (up, down, left, right, diagonal) is a blue (1) or orange (7) cell that has been changed to a 5 in the first pass, change the current cell's color to gray (5)

4. Otherwise, keep the original color of the cell.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Helper function to check neighbors for 1s and 7s
    def check_neighbors_1_7(r, c):
        for i in range(max(0, r - 1), min(rows, r + 2)):
            for j in range(max(0, c - 1), min(cols, c + 2)):
                if (i != r or j != c) and input_grid[i, j] != input_grid[r,c] and input_grid[i,j] != 8:
                    return True
        return False
    
    # helper function to check neighbors of 8
    def check_neighbors_8(r, c, changed_to_5):
      for i in range(max(0, r-1), min(rows, r + 2)):
        for j in range(max(0, c-1), min(cols, c+2)):
          if (i,j) in changed_to_5:
              return True
      return False

    # first pass change 1s and 7s
    changed_to_5 = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] in (1, 7):
                if check_neighbors_1_7(r, c):
                    output_grid[r, c] = 5
                    changed_to_5.append((r,c))

    # second pass change 8s
    for r in range(rows):
      for c in range(cols):
        if input_grid[r,c] == 8:
          if check_neighbors_8(r, c, changed_to_5):
            output_grid[r,c] = 5

    return output_grid