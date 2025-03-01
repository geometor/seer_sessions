# 97a05b5b • 004 • refine_coder

---
```python
"""
1.  **Change the Background:** Change all pixels in the input grid to red (color value 2).
2.  **Identify Sub-Objects:** Find all contiguous blocks (objects) of pixels that are *not* white (0) and *not* red (2) in the *original* input grid.
3.  **Preserve Sub-Object Colors:** For each identified sub-object, maintain its original color from the input grid in the now entirely red output grid. The locations and shapes of these sub-objects do *not* change.
"""

import numpy as np

def find_objects(grid, ignore_colors):
    """Finds contiguous objects of non-ignored colors."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(row, col, color, obj_coords):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        obj_coords.append((row, col))
        dfs(row + 1, col, color, obj_coords)
        dfs(row - 1, col, color, obj_coords)
        dfs(row, col + 1, color, obj_coords)
        dfs(row, col - 1, color, obj_coords)

    for row in range(rows):
        for col in range(cols):
            if not visited[row, col] and grid[row, col] not in ignore_colors:
                obj_coords = []
                dfs(row, col, grid[row, col], obj_coords)
                if obj_coords:
                    objects.append(obj_coords)
    return objects

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    # Initialize output_grid as a copy of the input, then change it all to red.
    output_grid = np.full_like(input_grid, 2)

    # Identify Sub-Objects in the *original* input grid
    ignore_colors = [0, 2]  # Ignore white and red
    sub_objects = find_objects(input_grid, ignore_colors)

    # Preserve Sub-Object Colors
    for obj_coords in sub_objects:
        for row, col in obj_coords:
            # Copy the original color from the input to the output
            output_grid[row, col] = input_grid[row, col]
            
    return output_grid
```
