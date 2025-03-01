# 623ea044 • 013 • refine_coder

---
```python
"""
1.  **Locate the Orange Pixel:** Search the input grid for an orange pixel (value 7). If no orange pixel is found, return an all-black (all zeros) grid of the same dimensions as the input.

2.  **Create Bounded Diagonals:** If an orange pixel is found at location (row, col):
    * Create two diagonal lines centered at that location.
    * The first diagonal runs from top-left to bottom-right.
    * The second diagonal runs from top-right to bottom-left.
    *   Extend the orange pixels along each diagonal *only up to the edges of the grid*. In other words, do not go beyond row 0, column 0, the maximum row index, or the maximum column index. This handles cases where the initial orange pixel is near an edge or corner.
    *   Where the diagonals intersect, the pixel is of course orange.

3. return the output grid.
"""

import numpy as np

def find_orange_pixel(grid):
    # Find the coordinates of the orange pixel (value 7)
    for r in range(len(grid)):
        for c in range(len(grid[0])):
          if grid[r][c] == 7:
            return (r, c)
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = len(input_grid), len(input_grid[0])

    # Find the original orange pixel
    orange_pixel_coords = find_orange_pixel(input_grid)

    if orange_pixel_coords:
      row, col = orange_pixel_coords

      # Create bounded diagonal cross
      # Top-left to bottom-right diagonal
      for i in range(min(rows, cols)):
          r, c = row - i, col - i
          if 0 <= r < rows and 0 <= c < cols:
              output_grid[r, c] = 7

          r, c = row + i, col + i
          if 0 <= r < rows and 0 <= c < cols:
              output_grid[r, c] = 7
      
      # Top-right to bottom-left
      for i in range(min(rows,cols)):
          r, c = row - i, col + i
          if 0 <= r < rows and 0 <= c < cols:
            output_grid[r,c] = 7
          
          r, c = row + i, col - i
          if 0 <= r < rows and 0 <= c < cols:
              output_grid[r,c] = 7

    # if no 7 found, return a black grid
    return output_grid
```
