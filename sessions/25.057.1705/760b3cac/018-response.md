# 760b3cac • 018 • refine_coder

---
```python
"""
1.  **Identify Azure Objects:** Locate all distinct azure (color 8) objects in the input grid. A distinct object is a set of contiguous azure pixels.
2.  **Process Each Azure Object:** For each azure object, consider its bounding box (the smallest rectangle that fully contains it).
3.  **Removal Rule**:
    *   If the azure object is a single pixel, remove it if and only if it is the top-left most single-pixel azure object.
    *   If there is only a single azure object that is greater than 1 pixel, then remove pixels to the left of the y-max, effectively keeping only the right-most part of the image.
    *   If there are multiple azure objects, remove any that are not the right-most objects.
4.  **Yellow Objects Unchanged:** Yellow (color 4) objects are not modified. Their positions and shapes remain the same in the output grid.
"""

import numpy as np

def find_objects(grid, color):
    coords = np.argwhere(grid == color)
    if len(coords) == 0:
        return []  # Return empty list if no objects of specified color
    # Group contiguous pixels into objects
    objects = []
    visited = set()
    for x, y in coords:
        if (x, y) not in visited:
            object_coords = []
            stack = [(x, y)]
            while stack:
                curr_x, curr_y = stack.pop()
                if (curr_x, curr_y) in visited:
                    continue
                visited.add((curr_x, curr_y))
                object_coords.append((curr_x, curr_y))
                # Check adjacent pixels (up, down, left, right)
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    new_x, new_y = curr_x + dx, curr_y + dy
                    if (0 <= new_x < grid.shape[0] and 0 <= new_y < grid.shape[1] and
                            grid[new_x, new_y] == color and (new_x, new_y) not in visited):
                        stack.append((new_x, new_y))
            objects.append(object_coords)
    return objects

def get_object_extents(obj):
    """returns xmin, xmax, ymin, ymax"""
    xmin = min(x for x, y in obj)
    xmax = max(x for x, y in obj)
    ymin = min(y for x, y in obj)
    ymax = max(y for x, y in obj)
    return xmin, xmax, ymin, ymax

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find objects of color 8 (azure) and 4 (yellow)
    azure_objects = find_objects(input_grid, 8)
    yellow_objects = find_objects(input_grid, 4)

    # Handle yellow objects (they remain unchanged)
    #   - already done by initializing with a copy of the input

    # Handle azure objects
    if len(azure_objects) > 0:
        if len(azure_objects) == 1 and len(azure_objects[0]) > 1: # One large azure object
            xmin, xmax, ymin, ymax = get_object_extents(azure_objects[0])
            for x, y in azure_objects[0]:
                if y < ymax:
                  output_grid[x,y] = 0
        elif len(azure_objects) > 1: # Multiple azure object
            #find rightmost object
            rightmost_ymax = -1
            for obj in azure_objects:
                _, _, _, ymax = get_object_extents(obj)
                rightmost_ymax = max(rightmost_ymax, ymax)

            for obj in azure_objects:
                xmin, xmax, ymin, ymax = get_object_extents(obj)
                if len(obj) == 1 and xmin == 0 and ymin == 0:  #top-left most object
                  output_grid[obj[0][0],obj[0][1]] = 0
                elif ymax < rightmost_ymax:
                  # remove all pixels
                  for x,y in obj:
                    output_grid[x,y] = 0

        elif len(azure_objects) == 1 and len(azure_objects[0]) == 1:  # single pixel object
          output_grid[azure_objects[0][0][0], azure_objects[0][0][1]] = 0
    return output_grid
```
