# 681b3aeb • 002 • example_1 • investigate_coder

---
```python
"""
The transformation rule extracts colored objects from the input grid, removes the white (0) background, and arranges them in a smaller grid, preserving their relative positions.
"""

import numpy as np

def find_objects(grid):
    # Find all contiguous non-zero regions in the grid.
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, color, object_pixels):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        object_pixels.append((r, c))
        dfs(r + 1, c, color, object_pixels)
        dfs(r - 1, c, color, object_pixels)
        dfs(r, c + 1, color, object_pixels)
        dfs(r, c - 1, color, object_pixels)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and not visited[r, c]:
                object_pixels = []
                dfs(r, c, grid[r, c], object_pixels)
                objects.append((grid[r, c], object_pixels))
    return objects

def transform(input_grid):
    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Extract colors and their positions
    colors = [color for color, _ in objects]
    positions = [pixels for _, pixels in objects]

    # Determine output grid size based on relative object positions
    min_r, min_c = 1000,1000
    max_r, max_c = -1,-1
    
    for object_pos in positions:
        for r,c in object_pos:
            min_r = min(r,min_r)
            max_r = max(r,max_r)
            
            min_c = min(c,min_c)
            max_c = max(c,max_c)

    # Create the output grid
    output_grid = np.zeros((max_r-min_r + 1, max_c - min_c + 1), dtype=int)

    # Place the objects in output
    for i, object_pixels in enumerate(positions):
        for r,c in object_pixels:
            output_grid[r-min_r, c-min_c] = colors[i]

    return output_grid
```
