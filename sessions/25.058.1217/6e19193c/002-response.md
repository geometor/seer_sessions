# 6e19193c • 002 • example_2 • investigate_coder

---
```python
"""
The transformation takes each colored block, and "scatters" its pixels into a diagonal line, 
keeping the relative position the same as the original form.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous blocks of non-white pixels."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, obj_pixels):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        obj_pixels.append((r, c))
        dfs(r + 1, c, color, obj_pixels)
        dfs(r - 1, c, color, obj_pixels)
        dfs(r, c + 1, color, obj_pixels)
        dfs(r, c - 1, color, obj_pixels)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                obj_pixels = []
                dfs(r, c, grid[r, c], obj_pixels)
                objects.append({'color': grid[r, c], 'pixels': obj_pixels})
    return objects

def center_of_mass(pixels):
    """Calculates the center of mass of a set of pixels."""
    if not pixels:
        return 0,0
    sum_r = sum(p[0] for p in pixels)
    sum_c = sum(p[1] for p in pixels)
    return round(sum_r / len(pixels)), round(sum_c / len(pixels))

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    
    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Scatter pixels of each object along a diagonal
    for obj in objects:
        pixels = obj['pixels']
        color = obj['color']
        center_r, center_c = center_of_mass(pixels)

        # Scatter the pixels diagonally
        for i, (r, c) in enumerate(pixels):
            new_r = center_r - len(pixels) // 2 + i
            new_c = center_c - len(pixels) // 2 + i

            if 0 <= new_r < output_grid.shape[0] and 0 <= new_c < output_grid.shape[1]:
                  output_grid[new_r, new_c] = color

    return output_grid
```
