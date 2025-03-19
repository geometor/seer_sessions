# b0c4d837 • 016 • example_3 • investigate_coder

---
```python
"""
Extracts the color of a centrally located azure object within an input grid and
places it on the top row of a 3x3 output grid.
The remaining cells of the output grid are filled with white (0).
"""

import numpy as np

def get_objects(grid):
    """
    Identify contiguous regions of the same color as distinct objects.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, color, obj_coords):
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
            if not visited[r, c]:
                obj_coords = []
                dfs(r, c, grid[r, c], obj_coords)
                if obj_coords:
                    objects.append(obj_coords)
    return objects

def transform(input_grid):
    # Initialize the output grid as 3x3 filled with white (0).
    output_grid = np.zeros((3, 3), dtype=int)

    # Get all objects in input grid
    objects = get_objects(input_grid)
    
    # find object with color 8 (azure)
    azure_object = None
    for obj in objects:
        first_pixel_color = input_grid[obj[0][0], obj[0][1]]
        if first_pixel_color == 8:
          azure_object = obj
          break
        
    if azure_object is None: # if no azure, return white grid
        return output_grid

    # fill top row with color of azure object
    output_grid[0, :] = 8

    return output_grid
```
