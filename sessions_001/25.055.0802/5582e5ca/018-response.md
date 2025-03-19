# 5582e5ca • 018 • refine_coder

---
```python
"""
1. Identify the colored square: Find the contiguous square region of non-white (non-zero) color within the input grid. This is the *target object*.
2. Preserve Dimensions: The output grid has the same dimensions as the input grid.
3. Replace Target with Magenta: Change the color of *all* pixels within the bounding box of the target object to magenta (color code 6).
4. Remove background: Change all the white background pixels to magenta.
"""

import numpy as np

def get_objects(grid):
    """
    Identifies distinct objects in a grid.  An object is a contiguous region
    of the same color.  Uses a simple flood-fill algorithm.
    """
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def flood_fill(row, col, color, object_pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1]
                or visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        object_pixels.append((row, col))
        flood_fill(row + 1, col, color, object_pixels)
        flood_fill(row - 1, col, color, object_pixels)
        flood_fill(row, col + 1, color, object_pixels)
        flood_fill(row, col - 1, color, object_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                color = grid[row, col]
                object_pixels = []
                flood_fill(row, col, color, object_pixels)
                if object_pixels:
                    objects.append({
                        'color': color,
                        'pixels': object_pixels,
                        'bounding_box': (min(p[0] for p in object_pixels), min(p[1] for p in object_pixels),
                                         max(p[0] for p in object_pixels), max(p[1] for p in object_pixels)),
                        'area': len(object_pixels)
                    })
    return objects

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find the colored square (target object)
    objects = get_objects(input_grid)
    target_object = None
    for obj in objects:
        if obj['color'] != 0:  # Non-white object
            # Check if it's a square (could be refined to check for perfect square)
            width = obj['bounding_box'][3] - obj['bounding_box'][1] + 1
            height = obj['bounding_box'][2] - obj['bounding_box'][0] + 1
            if width == height:
              target_object = obj
              break

    # if no target object found, return
    if target_object is None:
        return output_grid

    # Replace the target object's pixels with magenta (6)
    for row in range(target_object['bounding_box'][0], target_object['bounding_box'][2] + 1):
        for col in range(target_object['bounding_box'][1], target_object['bounding_box'][3] + 1):
            output_grid[row, col] = 6
            
    # replace background
    for row in range(output_grid.shape[0]):
      for col in range(output_grid.shape[1]):
        if output_grid[row,col] == 0:
          output_grid[row,col] = 6

    return output_grid
```
