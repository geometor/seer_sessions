# ef135b50 • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule identifies enclosed regions of red (2) pixels within the input grid and changes their color to maroon (9).
Enclosure here refers to the internal area with contiguous red pixels.
"""

import numpy as np

def get_objects(grid, color):
    # Find all objects of the specified color.
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, current_object):
        if (
            r < 0
            or r >= rows
            or c < 0
            or c >= cols
            or (r, c) in visited
            or grid[r, c] != color
        ):
            return
        visited.add((r, c))
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def is_enclosed(object_pixels, grid):
    """Checks if a connected region in a grid is fully enclosed."""
    # expanded_grid = np.pad(grid, pad_width=1, mode='constant', constant_values=0)

    rows, cols = grid.shape
    min_r, min_c = rows, cols
    max_r, max_c = -1, -1

    # find bounds of shape.
    for r, c in object_pixels:
      min_r = min(min_r, r)
      min_c = min(min_c, c)
      max_r = max(max_r, r)
      max_c = max(max_c, c)

    # check all pixels inside bounds for 0 (white space)
    for i in range(min_r, max_r + 1):
        for j in range(min_c, max_c + 1):
            if (i,j) not in object_pixels:
                if grid[i,j] == 0:
                    return False # not enclosed

    return True

def transform(input_grid):
    # Initialize output_grid with the same dimensions and data type as the input_grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Get all red objects
    red_objects = get_objects(input_grid, 2)

    # Fill enclosed red regions with maroon.
    for obj in red_objects:
      if is_enclosed(obj, input_grid):
        for r, c in obj:
              output_grid[r, c] = 9

    return output_grid
```
