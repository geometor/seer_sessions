# 41e4d17e • 006 • example_1 • investigate_coder

---
```python
"""
1.  Identify the blue cross shape in the input grid.
2.  Find the vertical center (y-axis center, i.e. row index) of the blue cross.
3.  Draw a vertical line of color 6 (magenta) across the entire height of the grid.
4.  The line should be placed that it intersects with the vertical center of the cross. Parts of the blue cross are replaced by magenta pixels.
5. All other color 8 (azure) pixels remain the same.
"""

import numpy as np

def find_object(grid, color):
    # find the coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    return coords

def find_center_y(coords):
    # find the vertical center (row index) of a set of coordinates
    if len(coords) == 0:
       return None
    y_coords = coords[:, 0]
    return (y_coords.min() + y_coords.max()) // 2
    

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # find blue cross
    cross_coords = find_object(input_grid, 1)
    
    # find y center
    center_y = find_center_y(cross_coords)

    # find the x coord of the center of the cross
    cross_x_coords = cross_coords[:,1]
    center_x = (cross_x_coords.min() + cross_x_coords.max()) // 2
    
    # draw vertical line on output_grid
    for y in range(output_grid.shape[0]):
      output_grid[y, center_x] = 6
    
    return output_grid
```
