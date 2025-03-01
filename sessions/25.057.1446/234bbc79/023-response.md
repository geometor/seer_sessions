# 234bbc79 • 023 • refine_coder

---
```python
"""
1. Identify Objects: Find all contiguous blocks of pixels of the same color. Consider these as distinct objects.
2. Identify Background: The background is color 8.
3. Isolate Small Objects: Identify objects composed of a single pixel.
4. Change small object color: change any single pixel object that isn't the background to color 0 (black)
"""

import numpy as np

def get_objects(grid):
    """Finds contiguous blocks of pixels with the same color."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_pixels):
        """Depth-first search to find contiguous pixels."""
        if (row < 0 or row >= grid.shape[0] or
            col < 0 or col >= grid.shape[1] or
            visited[row, col] or grid[row, col] != color):
            return

        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                obj_pixels = []
                dfs(row, col, grid[row, col], obj_pixels)
                if obj_pixels:
                    objects.append(obj_pixels)
    return objects


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Identify Objects
    objects = get_objects(input_grid)
    
    # Identify and change small objects
    for obj in objects:
      if len(obj) == 1:
        row, col = obj[0]
        if output_grid[row,col] != 8:
          output_grid[row,col] = 0

    return output_grid
```
