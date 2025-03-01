# 045e512c • 014 • example_3 • investigate_coder

---
```python
"""
The transformation identifies three objects: a grey 'C' shaped object (color 5), a magenta pixel (color 6), and a blue 'L' shaped object (color 1). The grey object remains unchanged. The magenta pixel is replicated diagonally upwards-right and downwards-left. The blue 'L' shaped object is also replicated diagonally, maintaining its shape and expanding.
"""

import numpy as np

def find_object(grid, color):
    # returns a list of coordinates where that makes up and object of given color
    coords = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r,c] == color:
                coords.append((r,c))
    return coords

def replicate_magenta(grid, start_r, start_c):
    # specific replication pattern for magenta (color 6)
    grid[start_r - 1, start_c + 1] = 6
    grid[start_r - 2, start_c + 2] = 6
    grid[start_r    , start_c + 2] = 6
    grid[start_r + 1, start_c - 1] = 6
    grid[start_r + 1, start_c + 1] = 6 # overlap here
    grid[start_r + 2, start_c - 2] = 6

def replicate_blue(grid, object_coords):
    # specific replication for blue, maintaining shape and expanding diagonally.
    min_r = min(r for r, c in object_coords)
    min_c = min(c for r, c in object_coords)

    # original is a 2x2 but one is cut off
    # create the shape, and translate as we replicate

    # diagonal upwards and right
    for i in range(1,3):
       for r_off in range(2):
          for c_off in range(2):
              if (min_r + r_off, min_c+c_off) in object_coords:
                 grid[min_r + r_off - i, min_c + c_off + i ] = 1

    # diagonal downwards and left
    for i in range(1,4):
       for r_off in range(3):
          for c_off in range(3):
            if min_r+r_off < grid.shape[0] and min_c+c_off < grid.shape[1] and grid[min_r + r_off,min_c+c_off]==1:
               if min_r+r_off+i < grid.shape[0] and min_c+c_off-i > 0:
                 grid[min_r + r_off+ i, min_c+c_off - i] =1


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # find objects
    grey_object = find_object(input_grid, 5)  # Grey object
    magenta_object = find_object(input_grid, 6)  # Magenta object
    blue_object = find_object(input_grid, 1)    # Blue object

    # Grey object - no change
    # (no action needed as we copied input_grid to output_grid)

    # Magenta object
    for r, c in magenta_object:
       replicate_magenta(output_grid, r, c)
    
    # Blue object
    replicate_blue(output_grid, blue_object)
       

    return output_grid
```
