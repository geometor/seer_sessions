# 47c1f68c • 004 • example_1 • investigate_coder

---
```python
"""
The transformation removes all blue pixels. The central vertical red line is reduced to only have two pixels on either side of the central horizontal line. 
The central horizontal red line is also reduced to only have two pixels on either side of the central vertical line.
"""

import numpy as np

def find_object(grid, color):
    obj_coords = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r,c] == color:
              obj_coords.append((r,c))
    return obj_coords

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    output_grid[:] = 0 # set to white

    # Remove blue pixels
    for r in range(input_grid.shape[0]):
      for c in range(input_grid.shape[1]):
        if input_grid[r,c] == 1:
          output_grid[r,c] = 0 #set to all white background

    # Find red pixels
    red_pixels = find_object(input_grid, 2)

    # Find center row and column
    center_row = input_grid.shape[0] // 2
    center_col = input_grid.shape[1] // 2
    
    # Filter vertical red line pixels
    for r, c in red_pixels:
        if c == center_col:
            if (center_row - 2) < r < (center_row) or (center_row) < r < (center_row + 3) :
                output_grid[r, c] = 2

    # Filter horizontal red line
    for r, c in red_pixels:
        if r == center_row:
             if (center_col - 2) < c < (center_col) or (center_col) < c < (center_col + 3):
                 output_grid[r,c] = 2

    return output_grid
```
