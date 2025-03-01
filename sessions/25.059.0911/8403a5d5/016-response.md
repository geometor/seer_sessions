# 8403a5d5 • 016 • example_3 • investigate_coder

---
```python
"""
1.  **Identify the Seed:** Locate the single yellow (4) pixel in the input grid.
2.  **Vertical and Horizontal Lines:**  Create vertical and horizontal lines of yellow (4) pixels passing through the seed pixel, extending to the edges of the grid.
3. **Alternating Fill:** Fill the remaining cells with alternating 4 and 0 such that cells adjacent to 4 are either 4 or 0 and never 5.
4.  **Corner Replacement:** In the four corners of resulting checkerboard of 4s and 0s, replace the 0 with 5, if a 4 exist there, the values stays a 4.
"""

import numpy as np

def find_seed(grid):
    # Find the coordinates of the yellow (4) pixel.
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value == 4:
                return (r, c)
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape

    # find seed pixel
    seed_row, seed_col = find_seed(input_grid)

    # create the yellow cross
    for r in range(rows):
      output_grid[r, seed_col] = 4
    for c in range(cols):
      output_grid[seed_row, c] = 4

    # alternating fill
    for r in range(rows):
        for c in range(cols):
            if output_grid[r,c] == 0:
                if (abs(r - seed_row) + abs(c - seed_col)) % 2 == 0:
                  output_grid[r,c] = 4


    # corner replacement
    if output_grid[0, 0] == 0:
      output_grid[0, 0] = 5
    if output_grid[0, cols-1] == 0:
      output_grid[0, cols-1] = 5
    if output_grid[rows-1, 0] == 0:
      output_grid[rows-1, 0] = 5
    if output_grid[rows-1, cols-1] == 0:
      output_grid[rows-1, cols-1] = 5

    return output_grid
```
