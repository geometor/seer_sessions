# d43fd935 • 004 • refine_coder

---
```python
"""
The transformation consists of two independent operations:
1.  Fill any 2x2 green square with blue.
2.  Expand any existing blue pixels by one cell in all orthogonal directions (up, down, left, right), replacing white pixels.
"""

import numpy as np

def find_2x2_green_squares(grid):
    """Finds the coordinates of all 2x2 green squares in the grid."""
    squares = []
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            if grid[r, c] == 3 and grid[r + 1, c] == 3 and \
               grid[r, c + 1] == 3 and grid[r + 1, c + 1] == 3:
                squares.append((r, c))
    return squares

def transform(input_grid):
    """Transforms the input grid according to the rule."""
    grid = np.array(input_grid)
    rows, cols = grid.shape
    output_grid = np.copy(grid)

    # 1. Fill 2x2 green squares with blue.
    squares = find_2x2_green_squares(grid)
    for r, c in squares:
        output_grid[r:r+2, c:c+2] = 1

    # 2. Expand blue pixels.
    blue_pixels = np.where(grid == 1)
    for r, c in zip(*blue_pixels):
        # Check adjacent cells (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = r + dr, c + dc
            if 0 <= new_row < rows and 0 <= new_col < cols and output_grid[new_row, new_col] == 0:
                output_grid[new_row, new_col] = 1

    return output_grid.tolist()
```
