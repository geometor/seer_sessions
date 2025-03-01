# 760b3cac • 018 • refine_coder

---
```python
"""
The transformation involves two distinct objects, colored yellow (4) and azure (8). The yellow object remains stationary. Its position in the input grid is the same in the output grid. The azure object is shifted horizontally to the left. The amount of the shift is determined by the space between the yellow and azure objects. The right-most pixel of the shifted azure block is placed one space to the left of the left-most pixel of the yellow block. The output grid consists of the stationary yellow object and the shifted azure object, with all other cells being black (0).
"""

import numpy as np

def find_objects(grid):
    # Find contiguous blocks of non-zero pixels
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, color, obj):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj.append([r, c])
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and not visited[r, c]:
                obj = []
                dfs(r, c, grid[r, c], obj)
                objects.append((grid[r, c], obj))  # Store color and object
    return objects

def calculate_shift(yellow_obj, azure_obj):
    #find left most pixel of yellow object
    yellow_left = min([c for r, c in yellow_obj])

    #find right most pixel of azure block
    azure_right = max([c for r, c in azure_obj])

    return azure_right - yellow_left + 1

def transform(input_grid):
    # Initialize output grid as a zero-filled grid
    output_grid = np.zeros_like(input_grid)

    # Find objects in the input grid
    objects = find_objects(input_grid)

    yellow_obj = None
    azure_obj = None

    for color, obj in objects:
        if color == 4:
            yellow_obj = obj
        elif color == 8:
            azure_obj = obj

    # Place Yellow Object
    if yellow_obj is not None:
        for r, c in yellow_obj:
            output_grid[r, c] = 4

    # Place Azure object
    if azure_obj is not None and yellow_obj is not None:
        shift = calculate_shift(yellow_obj, azure_obj)
        for r, c in azure_obj:
            new_c = c - shift
            if new_c >= 0:
              output_grid[r,new_c] = 8

    return output_grid
```
