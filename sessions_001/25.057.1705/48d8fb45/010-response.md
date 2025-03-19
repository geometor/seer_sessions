# 48d8fb45 • 010 • refine_coder

---
```python
"""
The transformation identifies the largest object in the input grid and replicates it in the output grid.
If there are multiple objects of the same largest size, it selects the one with the highest color value.
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

def get_object_color(grid, object_coords):
    """Returns color of object"""
    return grid[object_coords[0]]

def transform(input_grid):
    # Find all objects in the input grid
    objects = find_objects(input_grid)

    # If no objects, return an empty grid matching input size.
    if not objects:
        return np.zeros_like(input_grid, dtype=int)

    # Find the largest object(s)
    max_size = 0
    largest_objects = []
    for obj in objects:
      if len(obj) > max_size:
        max_size = len(obj)
        largest_objects = [obj]
      elif len(obj) == max_size:
        largest_objects.append(obj)

    # If multiple largest of same size, use highest color
    if len(largest_objects) > 1:
      highest_color = -1
      selected_object = None
      for obj in largest_objects:
        color = get_object_color(input_grid, obj[0])
        if color > highest_color:
            highest_color = color
            selected_object = obj
    else:
        selected_object = largest_objects[0]

    # Create an output grid of the same size as the input.
    output_grid = np.zeros_like(input_grid, dtype=int)
    # Copy the largest object to the output.
    for row, col in selected_object:
        output_grid[row, col] = input_grid[row, col]

    return output_grid
```
