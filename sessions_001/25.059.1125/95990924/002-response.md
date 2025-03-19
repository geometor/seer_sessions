# 95990924 • 002 • example_3 • investigate_coder

---
```python
"""
Identifies 2x2 gray squares in the input grid and places colored pixels (blue, red, green, yellow) around them in a specific pattern.
"""

import numpy as np

def find_gray_squares(grid):
    # Find all 2x2 gray squares in the grid.
    gray_squares = []
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            if grid[r, c] == 5 and grid[r + 1, c] == 5 and grid[r, c + 1] == 5 and grid[r + 1, c + 1] == 5:
                gray_squares.append((r, c))
    return gray_squares

def transform(input_grid):
    """
    Transforms the input grid by adding colored pixels around 2x2 gray squares.
    """
    output_grid = np.copy(input_grid)
    gray_squares = find_gray_squares(input_grid)

    for r, c in gray_squares:
        # Place colored pixels around the gray square.
        # blue: Top-Left
        if r > 0 and c > 0:
          output_grid[r - 1, c -1] = 1
        
        # red: Top-Right
        if r > 0 and c + 2 < output_grid.shape[1]:
          output_grid[r-1, c + 2] = 2
        
        # green: Bottom-Left
        if r + 2 < output_grid.shape[0] and c > 0 :
          output_grid[r + 2, c - 1] = 3

        # yellow: Bottom-Right
        if r + 2 < output_grid.shape[0] and c + 2 < output_grid.shape[1]:
          output_grid[r + 2, c + 2] = 4

    return output_grid
```

