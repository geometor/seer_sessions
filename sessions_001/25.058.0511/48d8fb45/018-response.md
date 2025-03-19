# 48d8fb45 • 018 • refine_coder

---
```python
"""
Identify all red objects in the input grid, extract a bounding box that encompasses all red objects, and return a new grid containing only the red pixels within that bounding box, with all other pixels set to white (0).
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

def get_bounding_box(objects):
    """
    Calculates the bounding box that encompasses all objects
    Returns (min_row, min_col, max_row, max_col).
    """
    if not objects:
        return (0, 0, -1, -1) #return an empty box
    all_pixels = [pixel for obj in objects for pixel in obj] #flatten pixel list
    min_row = min(p[0] for p in all_pixels)
    min_col = min(p[1] for p in all_pixels)
    max_row = max(p[0] for p in all_pixels)
    max_col = max(p[1] for p in all_pixels)
    return (min_row, min_col, max_row, max_col)

def transform(input_grid):
    # Find red objects
    red_objects = get_objects(input_grid, 2)

    # Determine bounding box for ALL red objects
    bounding_box = get_bounding_box(red_objects)
    min_row, min_col, max_row, max_col = bounding_box

    # Extract subgrid based on bounding box.
    output_grid = input_grid[min_row:max_row+1, min_col:max_col+1]
    
    #ensure only red and white (background) are in the output
    output_grid = np.where(output_grid == 2, 2, 0)

    return output_grid
```
