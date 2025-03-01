# 681b3aeb • 014 • example_3 • investigate_coder

---
```python
"""
Transforms the input grid by creating a 3x3 output grid.
The output grid represents a combined and minimized view of the green and blue objects,
where the top row represents the blue object, the middle row intermixes blue and green,
and the bottom row represents the green object.
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
                
def get_bounding_box(coords):
    """Calculates the bounding box for a set of coordinates."""
    min_r = min(r for r, c in coords)
    max_r = max(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_c = max(c for r, c in coords)
    return min_r, max_r, min_c, max_c

def transform(input_grid):
    # Find distinct colored objects.
    objects = get_objects(input_grid)
    
    # Initialize the output grid.
    output_grid = np.zeros((3, 3), dtype=int)

    # Sort objects by their minimum row index (top-most first).
    sorted_objects = sorted(objects.items(), key=lambda item: min(r for r, _ in item[1]['coords']))

    # Populate output grid rows based on sorted objects.
    # Top row
    if len(sorted_objects) > 0:
      output_grid[0, :] = sorted_objects[0][1]['color']

    # Bottom Row
    if len(sorted_objects) > 1:
      output_grid[2, :] = sorted_objects[-1][1]['color']
    
    # Middle Row
    if len(sorted_objects) > 1:
        output_grid[1,0] = sorted_objects[0][1]['color']
        output_grid[1,1] = sorted_objects[1][1]['color']
        output_grid[1,2] = sorted_objects[0][1]['color']

    
    return output_grid
```
