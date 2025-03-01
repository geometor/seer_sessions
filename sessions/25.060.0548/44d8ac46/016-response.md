# 44d8ac46 • 016 • example_3 • investigate_coder

---
```python
"""
Find the shape that looks like letter "H", locate the inner 2x2 block of the "H" and recolor it to red.
"""

import numpy as np

def find_h_shape(grid):
    # Find all gray (5) pixels
    gray_pixels = np.argwhere(grid == 5)
    
    # Find the bounding box of the gray pixels
    min_row = np.min(gray_pixels[:, 0])
    max_row = np.max(gray_pixels[:, 0])
    min_col = np.min(gray_pixels[:, 1])
    max_col = np.max(gray_pixels[:, 1])

    # Create a subgrid containing only the gray region
    subgrid = grid[min_row:max_row+1, min_col:max_col+1]

    #Check the structure of subgrid matches "H". Top and bottom rows are full and the middle rows only contains 2 pixels on left and right.
    rows,cols = subgrid.shape
    for r in range(rows):
      if r == 0 or r == rows -1 : #check the full pixels on top and botton
          if not np.all(subgrid[r,:] == 5):
            return None
      else:
        if not (np.all(subgrid[r,1:3] == 5) and np.all(subgrid[r,3:cols-2] == 0) and  np.all(subgrid[r,cols-2:cols] == 5)):
          return None
    
    # Extract center coordinates
    center_row = (min_row + max_row) // 2
    center_col = (min_col + max_col) // 2
    
    return center_row, center_col


def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    # Find the center of the "H" shape
    center_coords = find_h_shape(output_grid)

    if center_coords:
        center_row, center_col = center_coords
        # Recolor the 2x2 center region to red (2)
        output_grid[center_row-1:center_row+1, center_col:center_col+2] = 2

    return output_grid
```
