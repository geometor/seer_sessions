# 045e512c • 004 • refine_coder

---
```python
"""
The transformation rule involves replicating existing objects horizontally to the right, based on their color and initial width. Azure objects are replicated either once or twice, creating a total width of 2 or 3 times their original width. Green objects are replicated to have width based on their original width. Red objects are not changed.
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
    """Transforms the input grid according to the replication rules."""
    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Determine the maximum expansion needed
    max_expansion = 0
    for obj in objects:
      if obj["color"] == 8:
        initial_width = max(c[1] for c in obj["coords"]) - min(c[1] for c in obj["coords"]) + 1
        if initial_width <= 3:
            expansion = 3 * initial_width
        else:
            expansion = 2 * initial_width
        max_expansion = max(max_expansion,expansion)
      elif obj["color"] == 3:
        initial_width = max(c[1] for c in obj["coords"]) - min(c[1] for c in obj["coords"]) + 1

        if initial_width == 3:
          expansion = 3 * initial_width
        else:
          expansion = initial_width + 5
        max_expansion = max(max_expansion, expansion)

    # Initialize output grid with appropriate dimensions
    output_grid = np.zeros((input_grid.shape[0], max(input_grid.shape[1],max_expansion)), dtype=int)

    for obj in objects:
        if obj["color"] == 8:  # Azure
            # Replicate horizontally based on initial width
            min_r = min(c[0] for c in obj["coords"])
            min_c = min(c[1] for c in obj["coords"])
            initial_width = max(c[1] for c in obj["coords"]) - min_c + 1

            if initial_width <= 3:
                total_width = 3 * initial_width
            else:
                total_width = 2 * initial_width
            for r in range(min_r, max(c[0] for c in obj["coords"])+1):
              for c in range(min_c,min_c + total_width):
                  output_grid[r,c] = obj["color"]


        elif obj["color"] == 3:  # Green
            # Replicate horizontally based on initial width
            min_r = min(c[0] for c in obj["coords"])
            min_c = min(c[1] for c in obj["coords"])
            initial_width = max(c[1] for c in obj["coords"]) - min_c + 1

            if initial_width == 3:
              total_width = 3 * initial_width
            else:
              total_width = initial_width + 5

            for r in range(min_r,max(c[0] for c in obj["coords"])+1):
                for c in range(min_c, min_c + total_width):
                  output_grid[r,c] = obj["color"]

        elif obj["color"] == 2:  # Red
            # Copy the object without changes
            for r, c in obj["coords"]:
                output_grid[r, c] = obj["color"]


    return output_grid
```
