# 6aa20dc0 • 010 • refine_coder

---
```python
"""
1.  **Identify Objects:** Identify all distinct colored contiguous regions (objects) within the grid, excluding the blue background.
2.  **Identify Source and Target**: For each object that is not azure, locate the positions immediately to the *right* or *below* the object.
3.  **Conditional Color Change:** if the cell immediately to the right or below a non-azure object is azure, change the color of the azure cell to match the color of the non-azure object. More specifically:
    - If a non-azure object has an azure cell immediately to its *right*, change the azure cell's color to the color of that object.
    - If a non-azure object has an azure cell immediately *below* it, change the azure cell's color to the color of that object.
4. If both condition in step 3 applies, perform both transformations.
"""

import numpy as np

def get_objects(grid):
    """Find contiguous regions of non-blue pixels."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(r, c, color, obj_coords):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj_coords.append((r, c))
        dfs(r + 1, c, color, obj_coords)
        dfs(r - 1, c, color, obj_coords)
        dfs(r, c + 1, color, obj_coords)
        dfs(r, c - 1, color, obj_coords)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 1 and not visited[r, c]:
                obj_coords = []
                dfs(r, c, grid[r, c], obj_coords)
                objects.append({
                    'color': grid[r, c],
                    'coords': obj_coords
                })
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Get the objects in a list
    objects = get_objects(input_grid)

    # Iterate through each non-blue, non-azure object
    for obj in objects:
        if obj['color'] != 1 and obj['color'] != 8:  # Not blue and not azure
            for r, c in obj['coords']:
                # Check to the right
                if c + 1 < cols and input_grid[r, c + 1] == 8:
                    output_grid[r, c + 1] = obj['color']
                # Check below
                if r + 1 < rows and input_grid[r + 1, c] == 8:
                    output_grid[r + 1, c] = obj['color']

    return output_grid
```
