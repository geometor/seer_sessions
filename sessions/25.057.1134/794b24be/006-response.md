# 794b24be • 006 • refine_coder

---
```python
"""
1. Examine the Input: Check the input grid for non-zero pixels.
2. All Zero Case: If all pixels in the input grid are zero, the output grid
   should be a solid block where all the pixels are of color 0
3. Object identification Identify all non-zero pixels and treat each one as a distinct object.
4. Transformation (Non-Zero Case): if there are non-zero pixels, For each
   non-zero pixel:
   a. Change its color to red.
   b. Move it to the top-left corner (0, 0) of the output grid.
   c. repeat this process to fill up the grid.
5. Output: Return the modified grid.
"""

import numpy as np

def find_non_zero_pixels(grid):
    """Finds the coordinates of all non-zero pixels in a grid."""
    rows, cols = grid.shape
    non_zero_coords = []
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] != 0:
                non_zero_coords.append((i, j))
    return non_zero_coords

def transform(input_grid):
    # Initialize output grid with all zeros and same dimensions as input
    output_grid = np.zeros_like(input_grid)

    # Find all non-zero pixels in the input grid
    non_zero_pixels = find_non_zero_pixels(input_grid)

    # If all pixels are zero, return a copy of input grid, handles all zero case
    if not non_zero_pixels:
        return output_grid
    
    # handle the non-zero case
    # Place a red pixel at the top-left corner for each non zero pixel
    row_idx = 0
    col_idx = 0

    for _ in non_zero_pixels:
      if row_idx < output_grid.shape[0]:
          output_grid[row_idx, col_idx] = 2
          col_idx += 1
          if col_idx >= output_grid.shape[1]:
            col_idx = 0
            row_idx += 1

    return output_grid
```
