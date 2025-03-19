# 5614dbcf • 012 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find the rectangular, contiguous regions of red (color 2) and orange (color 7) pixels in the input grid.
2.  **Bounding Box:** Determine a bounding box that would contain both the red and orange regions.
3. **Create Output:** Create a new grid with the same dimensions of the bounding box.
4.  **Extract and Reposition:** Extract the red and orange regions. Place these regions into the output grid. The vertical order of the regions should be maintained (red above orange). The shape and size of the regions should be preserved.
5.  **Discard:** Remove all other colors, leaving only red, orange, and white (background, color 0).
"""

import numpy as np

def find_objects(grid, colors):
    # Find contiguous regions of specified colors
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_coords):
        # Depth-first search to find contiguous regions
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_coords.append((row, col))
        dfs(row + 1, col, color, obj_coords)
        dfs(row - 1, col, color, obj_coords)
        dfs(row, col + 1, color, obj_coords)
        dfs(row, col - 1, color, obj_coords)

    for color in colors:
        for r in range(grid.shape[0]):
            for c in range(grid.shape[1]):
                if grid[r, c] == color and not visited[r, c]:
                    obj_coords = []
                    dfs(r, c, color, obj_coords)
                    objects.append((color, obj_coords))
    return objects

def bounding_box(objects):
    #calculate a bounding box that contains all objects
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')

    for _, obj_coords in objects:
        for r, c in obj_coords:
            min_r = min(min_r, r)
            min_c = min(min_c, c)
            max_r = max(max_r, r)
            max_c = max(max_c, c)
    return (min_r, min_c), (max_r, max_c)

def transform(input_grid):
    # Find the red and orange objects
    objects = find_objects(input_grid, [2, 7])

    # Determine a bounding box for the objects
    (min_r, min_c), (max_r, max_c) = bounding_box(objects)
    
    # Create output grid based on the bounding box dimensions.
    output_grid = np.zeros((max_r - min_r + 1, max_c - min_c + 1), dtype=int)
    
    # reposition the objects in the ouput grid
    for color, obj_coords in objects:
       for r, c in obj_coords:
          output_grid[r-min_r,c-min_c] = color

    return output_grid
```
