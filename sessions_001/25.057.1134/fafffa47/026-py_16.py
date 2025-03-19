"""
1.  **Identify Objects:** Locate all distinct objects within the input grid. An object is a contiguous block of pixels with value other than 0.
2.  **Select Target Object:** Select the maroon (9) object.
3.  **Remove other objects:** The blue object is discarded.
4.  **Reduce Grid Size:** Create a new 3x3 output grid.
5.  **Simplify and Reposition Selected Object**: If in the original image, at least one pixel of the selected object appears on the first row in any of the three leftmost, or three rightmost pixels. Place a red pixel in the output grid at [0,0] if any of the three leftmost pixels is part of the object, and another pixel in the [0,2] position if any of the rightmost three pixel is part of the object.
6.  **Fill Background:** Fill the remaining cells of the output grid with white (0).
"""

import numpy as np

def find_objects(grid):
    # Find contiguous regions of non-zero pixels
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(r, c, color, obj_pixels):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                visited[r, c] or grid[r, c] != color):
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

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Select the maroon (9) object
    target_object = None
    for obj in objects:
        if obj['color'] == 9:
            target_object = obj
            break

    # Simplify and reposition
    if target_object:
        for r, c in target_object['pixels']:
          if r == 0:
            if c < 3:
              output_grid[0,0] = 2
            if c >= input_grid.shape[1]-3:
              output_grid[0,2] = 2
    return output_grid