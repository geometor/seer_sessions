# 1caeab9d • 010 • refine_coder

---
```python
"""
The transformation rule involves selectively moving objects down by one row based on their position relative to the top of the grid. Objects at the top of the grid (row 0) move down. Other objects remain in their original positions. The background color is white (0).

1.  **Identify Objects:** Find all contiguous blocks of the same color.
2.  **Check Top Row:** For each object, check if its top-most row is 0.
3.  **Move Down:** If an object's top row is 0, move it down by one row.
4.  **Keep Position:** If an object is not in the top row, keep its original position and dimensions.
5.  **Background:** The background color is white (0) and should be filled in appropriately wherever objects have moved.
"""

import numpy as np

def find_objects(grid):
    """Finds rectangular objects of uniform color."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, color, object_coords):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        object_coords.append((r, c))
        dfs(r + 1, c, color, object_coords)
        dfs(r - 1, c, color, object_coords)
        dfs(r, c + 1, color, object_coords)
        dfs(r, c - 1, color, object_coords)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c] and grid[r, c] != 0:
                object_coords = []
                dfs(r, c, grid[r, c], object_coords)
                # Determine object type (rectangle) and dimensions
                rows, cols = zip(*object_coords)
                min_row, max_row = min(rows), max(rows)
                min_col, max_col = min(cols), max(cols)
                objects.append({
                    'color': grid[r, c],
                    'coords': object_coords,
                    'top_left': (min_row, min_col),
                    'bottom_right': (max_row, max_col)
                })
    return objects

def move_object(grid, object_coords, dr, dc):
    """Moves an object by dr rows and dc columns."""
    new_coords = []
    for r, c in object_coords:
        new_coords.append((r + dr, c + dc))
    return new_coords

def transform(input_grid):
    # initialize output_grid with white (0)
    output_grid = np.zeros_like(input_grid)

    # Find all objects in the grid
    objects = find_objects(input_grid)

    # Process each object
    for obj in objects:
        # Check if the object is at the top row
        if obj['top_left'][0] == 0:
            # Move the object down by one row
            new_coords = move_object(input_grid, obj['coords'], 1, 0)
            for r, c in new_coords:
                if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                    output_grid[r, c] = obj['color']
        else:
            # Keep the object in its original position
            for r, c in obj['coords']:
                output_grid[r, c] = obj['color']

    return output_grid
```
