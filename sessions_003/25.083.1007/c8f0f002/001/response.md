```python
"""
Iterate through each cell of the input grid. For each cell, examine its
immediate neighbors (up, down, left, right, and diagonals).  If the current
cell has a value of 1 or 7, and at least one neighbor has a different value,
change the output value to 5. If the current cell has a value of 8, and is
adjacent to a cell with a value of 7 or 1 that has been changed in the output,
change the 8 to 5.  Otherwise, copy the cell's value from the input grid to
the output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Helper function to check neighbors
    def check_neighbors(r, c, value):
        for i in range(max(0, r - 1), min(rows, r + 2)):
            for j in range(max(0, c - 1), min(cols, c + 2)):
                if (i != r or j != c) and input_grid[i, j] != value:
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
                if check_neighbors(r, c, input_grid[r, c]):
                    output_grid[r, c] = 5
                    changed_to_5.append((r,c))

    # second pass change 8s
    for r in range(rows):
      for c in range(cols):
        if input_grid[r,c] == 8:
          if check_neighbors_8(r, c, changed_to_5):
            output_grid[r,c] = 5

    return output_grid
```