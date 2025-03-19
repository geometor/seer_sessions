# d4469b4b • 042 • refine_coder

---
```python
"""
The transformation identifies green (3) objects in a 5x5 input grid, changes their color to gray (5), and places them onto a 3x3 output grid, preserving their relative positions and shapes. All other pixels in the output grid remain black (0).
"""

import numpy as np

def get_objects(grid):
    """
    Finds contiguous regions (objects) of a specific color in the grid.
    Returns a list of objects, where each object is a list of (row, col) coordinates.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    
    def dfs(r, c, color, obj):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
            visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj.append((r, c))
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c] and grid[r,c] == 3: #look for green
                obj = []
                dfs(r, c, grid[r, c], obj)
                if obj:
                    objects.append(obj)
    return objects

def transform(input_grid):
    # Initialize output_grid as 3x3, filled with black (0)
    output_grid = np.zeros((3, 3), dtype=int)

    # Identify green objects in the input grid
    green_objects = get_objects(input_grid)

    # Transform and place objects onto the output grid
    for obj in green_objects:
        # Determine the relative position and shape
        
        for r, c in obj:
            # Map 5x5 input coordinates to 3x3 output coordinates. This preserves relative position.

            out_r = (r * 3) // 5 # simplified scaling - note, integer arithmetic
            out_c = (c * 3) // 5

            output_grid[out_r, out_c] = 5  # Change color to gray (5)

    return output_grid
```
