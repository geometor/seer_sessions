# 8f2ea7aa • 020 • refine_coder

---
```python
"""
1.  Examine Grid Dimensions: Determine the number of rows and columns of the input grid.
2.  Apply Transformation Rule:
    *   If both the number of rows and the number of columns are even, the output grid is completely filled with magenta (6), regardless of the input.
    *   If both the number of rows and columns are odd, and there is no existing 2x2 magenta square, output grid is filled with 6.
    *   If either the rows or columns is odd, the output grid is all zeros.
"""

import numpy as np

def find_2x2_squares(grid, color):
    """
    Finds all 2x2 squares of the specified color in the grid.
    """
    squares = []
    for r in range(grid.shape[0] - 1):
        for c in range(grid.shape[1] - 1):
            if (grid[r, c] == color and
                grid[r + 1, c] == color and
                grid[r, c + 1] == color and
                grid[r + 1, c + 1] == color):
                squares.append((r, c))
    return squares

def transform(input_grid):
    # initialize output_grid as all zeros
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # If both rows and cols are even, fill with 6s
    if rows % 2 == 0 and cols % 2 == 0:
        output_grid[:] = 6
    # If both rows and cols are odd
    elif rows % 2 != 0 and cols % 2 != 0:
        # Check for existing 2x2 magenta squares
        magenta_squares = find_2x2_squares(input_grid, 6)
        if not magenta_squares: # fill with 6s if there were *no* magenta squares
          output_grid[:] = 6
    # Otherwise output is already all zeros

    return output_grid
```
