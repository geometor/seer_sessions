```python
"""
Identifies blue (1) pixels that are part of a diagonal line of exactly three blue pixels and changes the center pixel to red (2).
"""

import numpy as np

def check_diagonal_line(grid, row, col):
    # check length 3 diagonal line
    is_diagonal = False
    
    # Check top-left to bottom-right diagonal
    if row > 0 and col > 0 and row < len(grid) - 1 and col < len(grid[0]) - 1:
      if grid[row-1][col-1] == 1 and grid[row+1][col+1] == 1:
        is_diagonal = True

    # Check top-right to bottom-left diagonal
    if row > 0 and col < len(grid[0]) - 1 and row < len(grid) -1 and col > 0:
      if grid[row-1][col+1] == 1 and grid[row+1][col-1] == 1:
        is_diagonal = True

    return is_diagonal
    

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Iterate through each pixel in the grid
    for row in range(rows):
        for col in range(cols):
            # Focus on blue pixels
            if input_grid[row][col] == 1:
                # Check if the blue pixel is part of a diagonal line of three blues
                if check_diagonal_line(input_grid, row, col):
                    output_grid[row][col] = 2

    return output_grid
```