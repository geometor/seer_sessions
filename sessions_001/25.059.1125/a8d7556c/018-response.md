# a8d7556c • 018 • refine_coder

---
```python
"""
1. Identify Objects: Find all 2x2 squares of gray (5) pixels in the input grid.
2. Transform: For each identified 2x2 gray square, change the color of all its pixels to red (2).
3. Output: Return the modified grid.
"""

import numpy as np

def find_2x2_gray_squares(grid):
    """Finds the top-left coordinates of all 2x2 gray squares in a grid."""
    rows, cols = grid.shape
    squares = []
    for i in range(rows - 1):
        for j in range(cols - 1):
            if (grid[i, j] == 5 and grid[i + 1, j] == 5 and
                grid[i, j + 1] == 5 and grid[i + 1, j + 1] == 5):
                squares.append((i, j))
    return squares

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find all 2x2 gray squares
    squares = find_2x2_gray_squares(output_grid)

    # Change the color of the pixels in each identified square to red (2)
    for row, col in squares:
        output_grid[row:row+2, col:col+2] = 2

    return output_grid
```
