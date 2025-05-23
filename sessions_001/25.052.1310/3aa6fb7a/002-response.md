# 1-3aa6fb7a • 002 • example_1 - CODE

---
```python
"""
The output preserves the azure colored object and adds a blue pixel adjacent to the azure object, to the right of its top-left corner, and one to the left of the bottom-right one.
"""

import numpy as np

def find_objects(grid, color):
    objects = []
    visited = set()

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # find azure objects
    azure_objects = find_objects(input_grid, 8)

    # add blue pixels
    for obj in azure_objects:
        # sort object coordinates to find top-left and bottom-right
        sorted_obj = sorted(obj, key=lambda x: (x[0], x[1]))
        top_left = sorted_obj[0]
        bottom_right = sorted_obj[-1]
        # adjust for the 2x1 vertical rectangle object shape assumption
        if len(obj) > 1 and top_left[0] == sorted_obj[1][0] -1 and top_left[1] == sorted_obj[1][1]:
            top_left_corner = top_left
        elif len(obj) > 1:
            top_left_corner = (sorted_obj[1][0], sorted_obj[1][1])
        else:
            top_left_corner = top_left
        
        if len(obj) > 1 and bottom_right[0] == sorted_obj[-2][0] + 1 and bottom_right[1] == sorted_obj[-2][1]:
           bottom_right_corner = bottom_right
        elif len(obj) > 1:
             bottom_right_corner = (sorted_obj[-2][0], sorted_obj[-2][1])
        else:
            bottom_right_corner = bottom_right

        #Add to the right of top left corner
        if top_left_corner[1] + 1 < output_grid.shape[1]:
          output_grid[top_left_corner[0], top_left_corner[1] + 1] = 1
        #Add to the left of the bottom right corner
        if bottom_right_corner[1] -1 >= 0:
          output_grid[bottom_right_corner[0], bottom_right_corner[1] - 1] = 1


    return output_grid
```
