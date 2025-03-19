# a8c38be5 • 008 • refine_coder

---
```python
"""
Identifies all distinct, colored objects in the input grid. Determines the
relative row and column offsets between these objects. Creates a new grid whose
dimensions are determined by the maximum relative offsets of any two objects.
Recreates the objects in the new grid, maintaining their relative positions and
filling any gaps created with the background color (0).
"""

import numpy as np

def find_objects(grid):
    """
    Identifies contiguous regions (objects) of the same color in a grid, excluding the background (0).
    Returns a list of objects, where each object is a tuple: (color, [(r, c), ...]).
    """
    objects = []
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, obj_coords):
        if (r, c) in visited or not is_valid(r, c) or grid[r][c] != color:
            return
        visited.add((r, c))
        obj_coords.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, color, obj_coords)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0 and (r, c) not in visited:
                color = grid[r][c]
                obj_coords = []
                dfs(r, c, color, obj_coords)
                objects.append((color, obj_coords))

    return objects

def transform(input_grid):
    # Find objects
    input_grid = np.array(input_grid)
    objects = find_objects(input_grid)

    if not objects:  # Handle the case where there are no objects
      return input_grid.tolist()

    # Get object coordinates
    object_coords = [obj[1] for obj in objects]

    # calculate the min/max row and col for all objects
    min_row = min([min([r for r, _ in obj]) for obj in object_coords])
    max_row = max([max([r for r, _ in obj]) for obj in object_coords])
    min_col = min([min([c for _, c in obj]) for obj in object_coords])
    max_col = max([max([c for _, c in obj]) for obj in object_coords])

    # determine output grid size
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    output_grid = np.zeros((height, width), dtype=int)

    # Place objects into output grid
    for color, coords in objects:
      for r,c in coords:
        output_row = r - min_row
        output_col = c - min_col
        output_grid[output_row, output_col] = color

    return output_grid.tolist()
```
