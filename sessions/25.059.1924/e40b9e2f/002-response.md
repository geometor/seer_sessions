# e40b9e2f • 002 • example_3 • investigate_coder

---
```python
"""
Identifies objects in a grid and expands them symmetrically outwards where the object borders 0-valued cells on opposite sides.
"""

import numpy as np

def get_objects(grid):
    """
    Find contiguous objects in the grid.
    Returns a list of objects, where each object is a set of (row, col) coordinates.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, obj_color, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != obj_color:
            return
        visited.add((r, c))
        current_object.add((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, obj_color, current_object)


    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_object = set()
                dfs(r, c, grid[r, c], current_object)
                objects.append((grid[r,c],current_object)) #store the color with the object.
    return objects

def transform(input_grid):
    """
    Transforms the input grid according to the symmetric expansion rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    objects = get_objects(input_grid)

    for color, obj in objects:
      for r, c in obj:
          # Check for symmetric expansion in horizontal and vertical directions.

            #vertical
          if r > 0 and r < rows - 1 and input_grid[r-1, c] == 0 and input_grid[r+1, c] == 0:
              output_grid[r-1,c] = input_grid[r,c]
              output_grid[r+1,c] = input_grid[r,c]

            #horizontal
          if c > 0 and c < cols - 1 and input_grid[r, c-1] == 0 and input_grid[r, c+1] == 0:
              output_grid[r,c-1] = input_grid[r,c]
              output_grid[r,c+1] = input_grid[r,c]

    return output_grid
```
