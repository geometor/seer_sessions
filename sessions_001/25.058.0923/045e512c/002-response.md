# 045e512c • 002 • example_1 • investigate_coder

---
```python
"""
The transformation rule involves replicating and extending existing objects, mostly to the right and sometimes downwards, based on their initial color. The azure and green objects are only extended to the right, while the red ones are extended both horizontally and vertically.
"""

import numpy as np

def find_objects(grid):
    """Finds distinct objects in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, color, obj_coords):
        """Depth-first search to find contiguous regions."""
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj_coords.append((r, c))
        dfs(r + 1, c, color, obj_coords)
        dfs(r - 1, c, color, obj_coords)
        dfs(r, c + 1, color, obj_coords)
        dfs(r, c - 1, color, obj_coords)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c] and grid[r, c] != 0:
                obj_coords = []
                dfs(r, c, grid[r, c], obj_coords)
                objects.append({
                    "color": grid[r, c],
                    "coords": obj_coords,
                })
    return objects

def transform(input_grid):
    """Transforms the input grid according to the replication and extension rules."""
    output_grid = np.zeros_like(input_grid)
    objects = find_objects(input_grid)

    for obj in objects:
        if obj["color"] == 8:  # Azure
            # Extend to the right
            min_r = min(c[0] for c in obj["coords"])
            max_r = max(c[0] for c in obj["coords"])
            min_c = min(c[1] for c in obj["coords"])
           # max_c = max(c[1] for c in obj["coords"])
            height = max_r - min_r + 1
            for r in range(min_r, min_r + height):
              for i in range(6):
                for c in range(min_c, min_c + 3):
                  if input_grid[r,c] != 0:
                    output_grid[r,min_c + i*3 + (c - min_c)] = obj["color"]

        elif obj["color"] == 3:  # Green
            # Extend to the right.
            min_r = min(c[0] for c in obj["coords"])
            min_c = min(c[1] for c in obj["coords"])

            for i in range(9):
                output_grid[min_r, min_c + i*2] = obj["color"]
                output_grid[min_r, min_c + 1 + i * 2 ] = obj["color"]
                output_grid[min_r, min_c + 2 + i*2 ] = obj["color"]


        elif obj["color"] == 2:  # Red
          #extend horizontally and vertically
            min_r = min(c[0] for c in obj["coords"])
            min_c = min(c[1] for c in obj["coords"])
            max_r = max(c[0] for c in obj["coords"])

            height = max_r - min_r + 1

            for j in range(3):
              for r in range(min_r, min_r + height * 3):
                for i in range(1):
                  for c in range(min_c, min_c+3):
                    if input_grid[r-j*height,c] != 0 and r < input_grid.shape[0]:
                      output_grid[r,c + i*3] = obj["color"]


    return output_grid
```
