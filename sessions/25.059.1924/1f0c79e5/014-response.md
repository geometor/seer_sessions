# 1f0c79e5 • 014 • refine_coder

---
```python
"""
1.  Identify all green (value 3) pixels in the input grid.
2.  Find the bounding box that perfectly contains the green.
3.  Iterate through every cell directly adjacent (up, down, left, right, and
    diagonals) to the original set of green cells.
4.  Check If an adjacent cell is white (value 0).
5.  Change adjacent white cells to green.
6.  Return the modified grid.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of all pixels of the specified color
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None, None, None
        
    #find top-left and bottom-right pixels to check for rectangular blocks
    min_row, min_col = np.min(coords, axis=0)
    max_row, max_col = np.max(coords, axis=0)
    
    return (min_row, min_col), (max_row, max_col), coords

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    grid_height = output_grid.shape[0]
    grid_width = output_grid.shape[1]

    # Find the green object
    top_left, bottom_right, green_coords = find_object(input_grid, 3)
    
    if top_left is None:
        return output_grid

    #create a set for faster checks, and so we dont recheck the same coord
    green_coords_set = set(tuple(coord) for coord in green_coords)

    # Iterate through the green coordinates
    for r, c in green_coords_set:
      #check adjacent cells - up, down, left, right and diagonals
      for dr in [-1,0,1]:
        for dc in [-1, 0, 1]:
          if dr == 0 and dc == 0:
            continue #skip the original cell
          
          nr, nc = r + dr, c + dc #neighbor row, col

          #boundary checks
          if 0 <= nr < grid_height and 0 <= nc < grid_width:
            #check if the adjacent is white
            if output_grid[nr, nc] == 0:
              output_grid[nr, nc] = 3 #set to green

    return output_grid
```
