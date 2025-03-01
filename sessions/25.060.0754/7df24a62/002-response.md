# 7df24a62 • 002 • example_4 • investigate_coder

---
```python
"""
This program identifies blue rectangles in a grid. If a blue rectangle contains yellow pixels,
it fills the interior of the rectangle with yellow and surrounds the yellow with a blue frame the
same width of the sides of the blue rectangle. Otherwise, the blue rectangle remains unchanged.
Isolated yellow pixels outside of any blue rectangle are preserved.
"""

import numpy as np

def get_objects(grid, color):
    # find contiguous regions of the specified color
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                obj = []
                stack = [(r, c)]
                visited[r, c] = True

                while stack:
                    curr_r, curr_c = stack.pop()
                    obj.append((curr_r, curr_c))

                    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        new_r, new_c = curr_r + dr, curr_c + dc
                        if 0 <= new_r < rows and 0 <= new_c < cols and \
                           grid[new_r, new_c] == color and not visited[new_r, new_c]:
                            stack.append((new_r, new_c))
                            visited[new_r, new_c] = True
                objects.append(obj)
    return objects

def get_bounding_box(obj):
    # calculate bounding box for an object
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')

    for r, c in obj:
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)

    return (min_r, min_c), (max_r, max_c)

def contains_color(grid, obj, color):
    # check if object contains specified color
    for r, c in obj:
        if grid[r,c] == color:
            return True
    return False
  
def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # get blue objects
    blue_objects = get_objects(input_grid, 1)
    
    # iterate and transform each blue rectangle object
    for blue_obj in blue_objects:
        # if object contains color yellow, switch it
        if contains_color(input_grid, blue_obj, 4):
            # get the top-left and bottom-right of the bounding box
            (min_r, min_c), (max_r, max_c) = get_bounding_box(blue_obj)
            # get side length of blue rectangle
            side_width = (max_r - min_r + 1) - (len([pt for pt in blue_obj if pt[0] == min_r]) -1)

            # convert blue object to have yellow center and blue border
            for r in range(min_r, max_r + 1):
                for c in range(min_c, max_c + 1):
                  # change every cell within bounding box to yellow
                    output_grid[r,c] = 4
            # create a blue frame of width `side_width`
            # create outer bounds for frame based on the side_width and original bounding box
            outer_min_r = min_r - side_width
            outer_min_c = min_c - side_width
            outer_max_r = max_r + side_width
            outer_max_c = max_c + side_width

            # set all within outer frame and not in original bounds to be blue.
            for r in range(outer_min_r, outer_max_r + 1):
              for c in range(outer_min_c, outer_max_c + 1):
                if (r < min_r or r > max_r) or (c < min_c or c > max_c):
                  # check bounds
                  if 0 <= r < rows and 0 <= c < cols:
                    output_grid[r,c] = 1

    return output_grid
```
