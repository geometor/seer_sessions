# 48d8fb45 • 002 • example_3 • investigate_coder

---
```python
"""
Identifies a non-white (0) and non-grey (5) object in the input grid, extracts its bounding box, and creates an output grid containing only that object's pixels, preserving relative positions.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects (non-0, non-5 pixels) in the grid.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c, color):
        return 0 <= r < rows and 0 <= c < cols and grid[r, c] == color and (r, c) not in visited

    def dfs(r, c, color, obj):
        visited.add((r, c))
        obj.append((r, c))

        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc, color):
                dfs(nr, nc, color, obj)

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0 and color != 5 and (r, c) not in visited:
                obj = []
                dfs(r, c, color, obj)
                objects.append((color, obj))
    return objects

def bounding_box(obj):
     """Calculates the bounding box of a list of coordinates."""
     min_r, min_c = float('inf'), float('inf')
     max_r, max_c = float('-inf'), float('-inf')
     for r, c in obj:
          min_r = min(min_r, r)
          min_c = min(min_c, c)
          max_r = max(max_r, r)
          max_c = max(max_c, c)
     return (min_r, min_c), (max_r, max_c)

def transform(input_grid):
    # Find all objects in input grid
    objects = find_objects(input_grid)

    # Find a valid object (not color 0 or 5)
    target_object = None
    target_color = 0

    for color, obj in objects:
      if color != 0 and color != 5:
          target_object = obj
          target_color = color
          break

    # if no object found, we return a 1x1 grid with 0
    if target_object is None:
      return np.zeros((1,1), dtype=int)

    # Determine bounding box coordinates
    (min_r, min_c), (max_r, max_c) = bounding_box(target_object)

    # Create the output grid
    output_grid = np.zeros((max_r - min_r + 1, max_c - min_c + 1), dtype=int)
    
    # Copy pixels within bounding box
    for r, c in target_object:
       output_grid[r-min_r, c-min_c] = target_color
    
    return output_grid
```
