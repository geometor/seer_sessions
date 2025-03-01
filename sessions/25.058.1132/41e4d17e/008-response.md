# 41e4d17e • 008 • refine_coder

---
```python
"""
1.  Identify the blue (color 1) object in the input grid.
2.  Find the horizontal center (x-axis center, i.e. column index) of the blue object.
3.  Draw a vertical line of color 6 (magenta) across the entire height of the grid.
4.  The line should be x coordinate of the horizontal center. The blue object may be partially or completely replaced with magenta pixels.
5. All other pixels remain the same.
"""

import numpy as np

def find_object(grid, color):
    # find the coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    return coords

def find_center_x(coords):
    # find the horizontal center (column index) of a set of coordinates
    if len(coords) == 0:
       return None
    x_coords = coords[:, 1]
    return (x_coords.min() + x_coords.max()) // 2
    

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # find blue object
    blue_coords = find_object(input_grid, 1)
    
    # find x center
    center_x = find_center_x(blue_coords)

    
    # draw vertical line on output_grid
    for y in range(output_grid.shape[0]):
      output_grid[y, center_x] = 6
    
    return output_grid
```
