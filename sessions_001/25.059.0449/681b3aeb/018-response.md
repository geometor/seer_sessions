# 681b3aeb • 018 • refine_coder

---
```python
"""
Transforms the input grid by creating a 3x3 output grid filled with the color of the single largest object found in the input. If multiple objects have the same largest size, the color of the object that appears first is used. If no objects are found (all background), the output is a 3x3 grid of the background color (0).
"""

import numpy as np

def get_objects(grid):
    """Finds distinct colored objects in the grid."""
    objects = {}
    visited = set()

    def dfs(r, c, color, obj_id):
        if (r, c) in visited or not (0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]) or grid[r, c] != color:
            return []
        visited.add((r, c))
        coords = [(r, c)]
        coords.extend(dfs(r + 1, c, color, obj_id))
        coords.extend(dfs(r - 1, c, color, obj_id))
        coords.extend(dfs(r, c + 1, color, obj_id))
        coords.extend(dfs(r, c - 1, color, obj_id))
        return coords

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            color = grid[r, c]
            if color != 0 and (r, c) not in visited:
                obj_id = len(objects) + 1
                objects[obj_id] = {
                    'color': color,
                    'coords': dfs(r, c, color, obj_id)
                }
    return objects

def transform(input_grid):
    # Find distinct colored objects.
    objects = get_objects(input_grid)

    # Determine output color (use the color of the largest object).
    output_color = 0  # Default to background color
    max_size = 0
    for obj_data in objects.values():
        size = len(obj_data['coords'])
        if size > max_size:
            max_size = size
            output_color = obj_data['color']

    # Create a 3x3 output grid filled with the determined color.
    output_grid = np.full((3, 3), output_color, dtype=int)

    return output_grid
```
