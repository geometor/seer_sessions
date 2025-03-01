# f76d97a5 • 011 • refine_coder

---
```python
"""
1.  **Initialization:** Start with a copy of the input grid.

2.  **Iteration:** Examine each pixel in the grid.

3.  **Conditional Change:**
    *   If a pixel is grey (5):
        *   If the pixel is at a corner of the grid, change it to black (0).
        *   If the pixel has at least 2, diagonally adjacent, grey(5) neighbors, change to black (0).
        *   Otherwise, keep its original color.
    *    If a pixel is not grey, keep the color.

4. **Output:** The modified grid is the output.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    def is_corner(row, col, rows, cols):
        return (row == 0 or row == rows - 1) and (col == 0 or col == cols - 1)

    def count_diagonal_grey_neighbors(row, col, grid):
        count = 0
        rows, cols = grid.shape
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 5:
                count += 1
        return count


    # change output pixels
    for row in range(rows):
        for col in range(cols):
            if output_grid[row, col] == 5:
                if is_corner(row, col, rows, cols):
                    output_grid[row, col] = 0
                elif count_diagonal_grey_neighbors(row, col, output_grid) >= 2:
                    output_grid[row,col] = 0

    return output_grid
```
