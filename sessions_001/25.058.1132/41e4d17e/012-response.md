# 41e4d17e • 012 • example_2 • investigate_coder

---
```python
"""
The transformation outlines each of the blue shapes with magenta, and it fills the space in any azure "channels" or areas between the blue shape and the created magenta border.
"""

import numpy as np

def get_objects(grid, color):
    """Find contiguous regions of the specified color."""
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(r, c, current_object):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def get_neighbors(grid, r, c):
    """Get the coordinates of neighboring pixels."""
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1]:
                neighbors.append((nr, nc))
    return neighbors
    

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find the blue objects
    blue_objects = get_objects(input_grid, 1)

    # Create a set of all blue pixel coordinates for easier lookup
    blue_pixels = set()
    for obj in blue_objects:
        blue_pixels.update(obj)


    # Iterate through all azure pixels
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r, c] == 8:  # If it's azure
                is_adjacent_to_blue = False
                for nr, nc in get_neighbors(input_grid, r, c):
                  if (nr,nc) in blue_pixels:
                    is_adjacent_to_blue = True
                    break

                if is_adjacent_to_blue:
                    output_grid[r,c] = 6
    
    
    #fill trapped azure pixels
    for r in range(input_grid.shape[0]):
      for c in range(input_grid.shape[1]):
        if output_grid[r,c] == 8:
          neighbors = get_neighbors(output_grid,r,c)
          all_magenta = True
          for nr, nc in neighbors:
            if output_grid[nr,nc] != 6 and output_grid[nr,nc] != 1:
              all_magenta = False
              break
          if all_magenta:
            output_grid[r,c] = 6
    
    return output_grid
```
