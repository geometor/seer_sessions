# 48d8fb45 • 012 • refine_coder

---
```python
"""
The transformation identifies the object in the input grid that contains the pixel at coordinates (5, 5).
If an object is found at that location, the entire object is copied to the output grid.
If no object contains (5, 5), the output grid is all zeros (empty).
"""

import numpy as np

def find_objects(grid):
    """
    Identifies distinct objects in the grid.
    Returns a list of objects, where each object is a list of (row, col) coordinates.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, current_object):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, color, current_object)
        dfs(row - 1, col, color, current_object)
        dfs(row, col + 1, color, current_object)
        dfs(row, col - 1, color, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                current_object = []
                dfs(row, col, grid[row, col], current_object)
                objects.append(current_object)
    return objects

def find_object_at_coordinate(objects, row, col):
    """
    Searches through a list of objects to find one containing a given coordinate.

    Args:
        objects: A list of objects, each represented as a list of (row, col) tuples.
        row: The row coordinate to search for.
        col: The column coordinate to search for.
    Returns:
        The object (list of coordinates) if found, otherwise None.

    """
    for obj in objects:
        if (row, col) in obj:
            return obj
    return None

def transform(input_grid):
    # Initialize output grid to all zeros (same size as input)
    output_grid = np.zeros_like(input_grid, dtype=int)

    # Find all objects in the input grid
    objects = find_objects(input_grid)

    # Find the object containing the pixel at (5, 5)
    target_object = find_object_at_coordinate(objects, 5, 5)

    # If an object is found at (5, 5), copy it to the output grid
    if target_object:
        for row, col in target_object:
            output_grid[row, col] = input_grid[row, col]

    return output_grid
```
