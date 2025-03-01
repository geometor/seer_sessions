# fafffa47 • 030 • refine_coder

---
```python
"""
1.  **Identify Objects:** Locate all distinct objects within the input grid. An object is a contiguous block of pixels with a value other than 0.
2.  **Select Target Object:** Select the maroon (9) object. Discard all the other objects.
3.  **Create Output Grid:** Create a new 3x3 output grid filled with white (0).
4. **Determine Red Pixel Column:** Check the horizontal position of the maroon object within the input image. If the object is in the left third of the input grid, place a red pixel at `[0, 0]` of the output grid. If the object is in the middle third, place a red pixel at `[0, 1]`. If the object is in the right third, place it on `[0,2]`.
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
    # Initialize output_grid (3x3 and filled with white)
    output_grid = np.zeros((3, 3), dtype=int)

    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Select the maroon (9) object
    target_object = None
    for obj in objects:
        if obj['color'] == 9:
            target_object = obj
            break

    # Determine Red Pixel Column and set the pixel
    if target_object:
        min_col = min(c for r, c in target_object['pixels'])
        max_col = max(c for r, c in target_object['pixels'])
        avg_col = (min_col + max_col) / 2
        input_width = input_grid.shape[1]

        if avg_col < input_width / 3:
            output_grid[0, 0] = 2  # Left third
        elif avg_col < 2 * input_width / 3:
            output_grid[0, 1] = 2  # Middle third
        else:
            output_grid[0, 2] = 2  # Right third

    return output_grid
```
