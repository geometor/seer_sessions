# a78176bb • 012 • refine_coder

---
```python
"""
1. Remove Gray Object: If a gray object (color 5) exists in the input grid, remove it by changing its pixels to white (color 0).

2. Transform Maroon Object: If a maroon object (color 9) exists in the input grid:
   * If the maroon object is part of a shape that includes a gray object connected on the left, then the maroon section remains and the gray section is removed.
   * Otherwise, transform the maroon object into a horizontal line of maroon pixels.
   * The length of the horizontal line is equal to the height + width of the input maroon object.
   * The y-coordinate of the horizontal line is equal to the maroon object's minimum y.
   * The x-coordinate of the new line is equal to original object bounds, minus 1.
"""

import numpy as np

def find_object(grid, value):
    coords = np.argwhere(grid == value)
    return coords

def get_object_bounds(coords):
    if len(coords) == 0:
        return None
    min_x = np.min(coords[:, 0])
    max_x = np.max(coords[:, 0])
    min_y = np.min(coords[:, 1])
    max_y = np.max(coords[:, 1])
    return (min_x, min_y, max_x, max_y)

def get_object_dimensions(coords):
  bounds = get_object_bounds(coords)
  if bounds is None:
    return (0,0)
  return (bounds[2] - bounds[0] + 1, bounds[3] - bounds[1] + 1)

def is_connected(gray_coords, maroon_coords):
    # check that gray and maroon form contiguous object
    if len(gray_coords) == 0 or len(maroon_coords) == 0:
        return False

    for g_x, g_y in gray_coords:
        for m_x, m_y in maroon_coords:
            if abs(g_x - m_x) <= 1 and abs(g_y - m_y) <=1:
              return True
    return False

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    input_grid = np.array(input_grid)

    # find gray object
    gray_coords = find_object(input_grid, 5)
    # Remove Gray Object
    for x, y in gray_coords:
        output_grid[x, y] = 0

    # find maroon object
    maroon_coords = find_object(input_grid, 9)
    if len(maroon_coords) == 0:
        return output_grid

    maroon_bounds = get_object_bounds(maroon_coords)
    maroon_dims = get_object_dimensions(maroon_coords)

    # check if they form a single shape
    if is_connected(gray_coords, maroon_coords):
      return output_grid

    # Transform Maroon object into horizontal line.
    new_length = maroon_dims[0] + maroon_dims[1]
    min_x, min_y, _, _ = maroon_bounds
    start_x = min_x -1

    # remove the existing maroon object
    for x,y in maroon_coords:
      output_grid[x,y] = 0

    for i in range(new_length):
        new_x = start_x + i
        if 0 <= new_x < output_grid.shape[0] and 0 <= min_y < output_grid.shape[1]:
          output_grid[new_x, min_y] = 9

    return output_grid
```
