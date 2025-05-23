# 045e512c • 018 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find three distinct objects: a grey "C" shaped object (color 5), a magenta pixel (color 6), and a blue "L" shaped object (color 1).

2.  **Grey Object Transformation:** The grey "C" shaped object remains unchanged in both position and shape.

3.  **Magenta Pixel Transformation:** The magenta pixel replicates *twice*. One replica appears one step diagonally *upwards and to the right* of the original. The second replica appears one step *downwards and to the left* of the original.

4.  **Blue "L" Object Transformation:** The blue "L" shaped object extends its vertical component diagonally. It adds one blue pixel *upwards and to the right*, and one blue pixel *downwards and to the left*, maintaining its original shape and relative position to the "L" shape. The extension is only for the "vertical bar" of the L shape.
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
    if start_r - 1 >= 0 and start_c + 1 < grid.shape[1]:
        grid[start_r - 1, start_c + 1] = 6
    if start_r + 1 < grid.shape[0] and start_c - 1 >= 0:
        grid[start_r + 1, start_c - 1] = 6


def replicate_blue(grid, object_coords):
    # specific replication for blue, maintaining shape and expanding diagonally.
    min_r = min(r for r, c in object_coords)
    min_c = min(c for r, c in object_coords)
    max_r = max(r for r,c in object_coords)

    # diagonal upwards and right
    if min_r - 1 >= 0 and max_r -1 >= 0 and min_c + 1 < grid.shape[1]:
        # check if this position has an 'L' shape
        if (min_r, min_c) in object_coords:
          grid[min_r - 1, min_c + 1] = 1

    # diagonal downwards and left, just extend the vertical line.
    if max_r + 1 < grid.shape[0] and min_c -1 >= 0:
        if (max_r, min_c) in object_coords:
            grid[max_r + 1,min_c-1] = 1


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
