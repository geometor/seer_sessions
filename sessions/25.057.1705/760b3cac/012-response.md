# 760b3cac • 012 • refine_coder

---
```python
"""
Identify the azure (8) object and the yellow (4) object.
Expand the azure object to fill the bounding box defined by its initial extent.
The yellow object remains unchanged.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous blocks of pixels with the same color.
    Returns a dictionary of objects, keyed by color.
    """
    objects = {}
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                color = grid[row, col]
                obj_pixels = []
                dfs(row, col, color, obj_pixels)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj_pixels)
    return objects

def get_bounding_box(pixels):
    """
    Calculates the bounding box of a set of pixels.
    Returns (min_row, min_col, max_row, max_col).
    """
    if not pixels:
        return None

    min_row = min(p[0] for p in pixels)
    max_row = max(p[0] for p in pixels)
    min_col = min(p[1] for p in pixels)
    max_col = max(p[1] for p in pixels)

    return (min_row, min_col, max_row, max_col)

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Check if azure (8) exists in the objects
    if 8 not in objects:
        return output_grid

    # Iterate through each azure object (in this case, expect only 1)
    for azure_object in objects[8]:
        # Get bounding box
        bounding_box = get_bounding_box(azure_object)
        if bounding_box is None:
            continue

        min_row, min_col, max_row, max_col = bounding_box

        # Fill the bounding box with azure (8)
        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                output_grid[row, col] = 8

    return output_grid
```
