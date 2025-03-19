# 445eab21 • 008 • example_2 • investigate_coder

---
```python
"""
1. Identify Objects: Locate all distinct colored regions within the input grid.
2. Select Color: Select the orange (7) object. Ignore all others.
3. Simplify Shape: Select a 2x2 square of orange colored pixels, ignoring the rest.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies distinct objects in a grid based on color contiguity.
    Returns a dictionary of objects, where the key is the color 
    and the value is a list of (row, col) coordinates.
    """
    objects = {}
    visited = set()

    def dfs(row, col, color, obj_coords):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        obj_coords.append((row, col))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(row + dr, col + dc, color, obj_coords)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            color = grid[row, col]
            if color != 0 and (row, col) not in visited:  # Exclude background color 0
                obj_coords = []
                dfs(row, col, color, obj_coords)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj_coords)
    return objects

def transform(input_grid):
    """
    Transforms the input grid according to the described rules.
    """
    # Find all objects in the grid
    objects = find_objects(input_grid)

    # Select the orange (7) object
    if 7 in objects:
      orange_objects = objects[7]
      #in case there's more than 1 object, choose first
      largest_orange_object = max(orange_objects, key=len, default=[])


      # Find a 2x2 square within the orange object
      output_grid = np.zeros((2, 2), dtype=int)

      #try and fill from top left of largest orange object.
      if len(largest_orange_object) >= 4:
        coords = sorted(largest_orange_object)
        output_grid[0,0] = 7
        output_grid[0,1] = 7
        output_grid[1,0] = 7
        output_grid[1,1] = 7
        

    else:
      output_grid = np.zeros((2, 2), dtype=int)

    return output_grid
```
