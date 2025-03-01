# 72322fa7 • 002 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Objects:** Find all contiguous regions of non-zero pixels in the input grid.
2.  **Mirror some Objects at the edge:**
    *   If there is some colored sub-grid at the border, mirror the sub-grid to the opposite border.
    *   If a colored pixel is not at the border, maintain the color.
3. Result is the output.
"""

import numpy as np

def get_objects(grid):
    """
    Finds contiguous regions of non-zero pixels (objects) in the grid.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_pixels):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] != 0 and not visited[row, col]:
                obj_pixels = []
                dfs(row, col, grid[row, col], obj_pixels)
                objects.append(
                    {"color": grid[row, col], "pixels": obj_pixels}
                )
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    h, w = input_grid.shape

    # change output pixels
    for r in range(h):
        for c in range(w):
            # If a colored pixel is not at the border, maintain the color
            if input_grid[r,c] != 0 and r > 0 and r < h - 1 and c > 0 and c < w-1:
                output_grid[r,c] = input_grid[r,c]
    
    # Find objects
    objects = get_objects(input_grid)

    # Mirror objects at the edge
    for obj in objects:
      pixels = obj['pixels']
      color = obj['color']

      for r,c in pixels:
        if r == 0: #top edge
            output_grid[h-1-r,c] = color
        elif r == h-1: # bottom edge
            output_grid[h-1-r,c] = color

        if c == 0: # left edge
            output_grid[r, w-1-c] = color
        elif c == w-1: # right edge
            output_grid[r, w-1-c] = color
            
    return output_grid
```
