# 48d8fb45 • 014 • example_3 • investigate_coder

---
```python
"""
Isolate a specific red object, extract a bounding box around the object, and return this as the new grid.
"""

import numpy as np

def get_objects(grid, color):
    """
    Finds contiguous regions of the specified color in the grid.
    Returns a list of objects, where each object is a list of (row, col) coordinates.
    """
    visited = set()
    objects = []

    def dfs(row, col, current_object):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and (row, col) not in visited:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def get_bounding_box(obj):
    """
    Calculates the bounding box of a given object (list of coordinates).
    Returns (min_row, min_col, max_row, max_col).
    """
     
    min_row = min(p[0] for p in obj)
    min_col = min(p[1] for p in obj)
    max_row = max(p[0] for p in obj)
    max_col = max(p[1] for p in obj)
    return (min_row, min_col, max_row, max_col)

def transform(input_grid):
    # Find red objects
    red_objects = get_objects(input_grid, 2)

    # if no red objects, return an empty grid
    if not red_objects:
        return np.zeros((0,0), dtype=int)

    # Determine bounding box for the first red object (per top-left rule in description)
    bounding_box = get_bounding_box(red_objects[0])
    min_row, min_col, max_row, max_col = bounding_box

    # Extract subgrid based on bounding box.
    output_grid = input_grid[min_row:max_row+1, min_col:max_col+1]
    
    #ensure only red and white (background) are in the output
    output_grid = np.where(output_grid == 2, 2, 0)

    return output_grid
```
