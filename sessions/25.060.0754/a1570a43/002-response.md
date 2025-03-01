# a1570a43 • 002 • example_4 • investigate_coder

---
```python
"""
The transformation rotates a shape made of red (2) pixels 90 degrees clockwise while keeping green (3) and white (0) pixels unchanged.
"""

import numpy as np

def get_red_shape(grid):
    """
    Extracts the coordinates of red pixels (value 2) forming the shape.
    """
    red_pixels = []
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value == 2:
                red_pixels.append((r, c))
    return red_pixels

def rotate_point(point, origin):
    """
    Rotates a point 90 degrees clockwise around an origin.
    """
    ox, oy = origin
    px, py = point

    qx = ox + (py - oy)
    qy = oy - (px - ox)
    return qx, qy

def get_rotation_origin(red_pixels):
    """
    Calculates an approximate "center" of rotation for the red shape.
    Uses the average (centroid) of the red pixels as the rotation origin
    """

    if not red_pixels:
       return (0,0)

    sum_x = 0
    sum_y = 0
    for x, y in red_pixels:
        sum_x += x
        sum_y += y
    return (round(sum_x / len(red_pixels)), round(sum_y / len(red_pixels)))

def transform(input_grid):
    # initialize output_grid
    output_grid = np.array(input_grid, copy=True)

    # get red shape coordinates
    red_pixels = get_red_shape(input_grid)
    
    # handle empty red pixels
    if not red_pixels:
        return output_grid

    # calculate the origin (centroid) of the red pixels
    origin = get_rotation_origin(red_pixels)

    # rotate red pixels and update the output_grid
    rotated_red_pixels = []
    for point in red_pixels:
      rotated_pixel = rotate_point(point,origin)
      rotated_red_pixels.append(rotated_pixel)

    # clear original red pixels
    for r,c in red_pixels:
      output_grid[r][c] = 0

    # add rotated pixels
    for r,c in rotated_red_pixels:
      # check if the cell within grid bounds
      if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
        output_grid[r][c] = 2

    return output_grid.tolist()
```
