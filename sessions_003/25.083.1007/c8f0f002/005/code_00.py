"""
1.  **First Pass (1s and 7s):**
    *   Iterate through each cell in the input grid.
    *   If a cell is blue (1) or orange (7):
        *   Check its immediate neighbors (up, down, left, right, and diagonals).
        *   If a neighboring cell has the *other* of these two colors (i.e., a 1 is next to a 7, or a 7 is next to a 1), change the current cell's color to gray (5).
        *   Keep track of these changed cells.
2.  **Second Pass (8s):**
    *   Iterate through each cell in the input grid.
    *   If a cell is azure (8):
        *   Check its immediate neighbors (up, down, left, right, and diagonals)
        *   If *any* neighbor was a 1 or 7 that changed to a 5 in the first pass, change the current cell (the 8) to gray (5).
3.  **All Other Cells:**
    *   Any cell not meeting the above conditions retains its original color.
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
                if (i != r or j != c):
                    if (input_grid[r,c] == 1 and input_grid[i,j] == 7) or \
                       (input_grid[r,c] == 7 and input_grid[i,j] == 1):
                        return True
        return False

    # helper function to check neighbors of 8
    def check_neighbors_8(r, c, changed_to_5):
      for i in range(max(0, r-1), min(rows, r + 2)):
        for j in range(max(0, c-1), min(cols, c+2)):
          if (i != r or j != c) and (i,j) in changed_to_5:  #check if neighbor is in the changed list
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