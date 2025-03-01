# 47c1f68c • 006 • refine_coder

---
```python
"""
1. Remove Blue: Eliminate all blue pixels from the input grid.
2. Find Center: Determine the center row and column of the grid.
3. Construct Red Cross: if there is a red cross shape centered in the grid, it is reduced to a 5x5 cross, maintaining its original center.
4. Remove Other Red: remove all other red shapes that are not the center cross.
"""

import numpy as np

def find_object(grid, color):
    obj_coords = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r,c] == color:
              obj_coords.append((r,c))
    return obj_coords

def is_cross(red_pixels, center_row, center_col):
    # Check if there are red pixels forming a cross shape
    horizontal = False
    vertical = False
    for r, c in red_pixels:
        if r == center_row:
            horizontal = True
        if c == center_col:
            vertical = True
    return horizontal and vertical

def transform(input_grid):
    # Initialize output grid as a copy of the input grid, then set all to 0 (white)
    output_grid = np.copy(input_grid)
    output_grid[:] = 0

    # Remove blue pixels
    for r in range(input_grid.shape[0]):
      for c in range(input_grid.shape[1]):
        if input_grid[r,c] == 1:
          output_grid[r,c] = 0

    # Find red pixels
    red_pixels = find_object(input_grid, 2)

    # Find center row and column
    center_row = input_grid.shape[0] // 2
    center_col = input_grid.shape[1] // 2

    # Check for a red cross and construct 5x5 red cross
    if is_cross(red_pixels, center_row, center_col):
      for r in range(center_row - 2, center_row + 3):
          for c in range(center_col - 2, center_col + 3):
              if 0 <= r < output_grid.shape[0] and 0<= c < output_grid.shape[1]:
                output_grid[r,c] = 2
    else: #remove all red pixels if no cross
        for r in range(input_grid.shape[0]):
            for c in range(input_grid.shape[1]):
                if output_grid[r,c] == 2:
                  output_grid[r,c] = 0

    return output_grid
```
