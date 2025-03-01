# 7f4411dc • 002 • example_3 • investigate_coder

---
```python
"""
Identify and remove single-pixel objects from the input grid, preserving larger connected objects.
"""

import numpy as np

def get_objects(grid):
    """
    Identifies distinct objects in the grid.
    """
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                dfs(r + dr, c + dc, color, current_object)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != 0:
                color = grid[r, c]
                current_object = []
                dfs(r, c, color, current_object)
                if color not in objects:
                    objects[color] = []
                objects[color].append(current_object)
    return objects

def transform(input_grid):
    """
    Transforms the input grid by removing single-pixel objects.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Get all objects in the grid
    objects = get_objects(output_grid)

    # Filter single-pixel objects
    for color, object_list in objects.items():
        for obj in object_list:
            if len(obj) == 1:
                # Remove single-pixel object
                r, c = obj[0]
                output_grid[r, c] = 0
            
    return output_grid
```
