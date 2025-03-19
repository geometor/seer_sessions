# 1f0c79e5 • 012 • refine_coder

---
```python
"""
If a green cluster exists, extend it by adding green
pixels.  Add pixels directly below each original green pixel.
Also, add two pixels to the right.  The original green
pixels should be unchanged.
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
    output_grid = np.copy(input_grid)
    
    # Find the green object
    top_left, bottom_right, green_coords = find_object(input_grid, 3)

    if top_left is not None:
      #get grid height
      grid_height = output_grid.shape[0]
      grid_width = output_grid.shape[1]
      
      #iterate through green pixels
      for coord in green_coords:
        #add green below
        for i in range(coord[0]+1,grid_height):
          output_grid[i][coord[1]]=3
        
        #add two green to the right
        if coord[1] + 2 < grid_width:
            output_grid[coord[0]][coord[1]+2] = 3
        

    return output_grid
```
