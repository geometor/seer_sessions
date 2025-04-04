# 1f0c79e5 • 010 • example_2 • investigate_coder

---
```python
"""
Transforms a green cluster in the input grid into an "L" shape that extends to the bottom-right corner of the grid.
Single red pixels are removed.
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
    """
    Transforms the input grid according to the described rule.
    """
    output_grid = np.zeros_like(input_grid)
    
    # Find the green object
    top_left, bottom_right, green_coords = find_object(input_grid, 3)

    if top_left is not None:
      #get grid height
      grid_height = output_grid.shape[0]
      
      #fill L shape
      for i in range(top_left[0],grid_height):
        output_grid[i][top_left[1]+2]=3
      for i in range(top_left[1],grid_height):
        output_grid[grid_height-1][i]=3

    return output_grid
```
