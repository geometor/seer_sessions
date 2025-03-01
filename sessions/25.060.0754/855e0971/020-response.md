# 855e0971 • 020 • refine_coder

---
```python
"""
1.  **Identify Objects:** Divide the input grid into distinct objects. An object is a contiguous block of pixels of the same color.
2.  **Count White Pixels:** For each object, count the number of white pixels. This count is the "replication factor" for that object.
3.  **Replicate All Object Rows:** For each object, replicate *all* of its rows. The number of times each row is replicated is equal to the object's replication factor (the white pixel count).
4.  **Construct Output:** Combine the replicated rows of all objects, preserving the original order of objects and the order of rows within each object, to form the final output grid.
"""

import numpy as np

def find_objects(grid):
    # Find distinct objects in the grid.
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, color, current_object):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, color, current_object)
        dfs(r - 1, c, color, current_object)
        dfs(r, c + 1, color, current_object)
        dfs(r, c - 1, color, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c]:
                current_object = []
                dfs(r, c, grid[r, c], current_object)
                objects.append(current_object)
    return objects

def count_white_pixels(grid, object_coords):
    # Count white pixels within a specific object.
    count = 0
    for r, c in object_coords:
        if grid[r, c] == 0:
            count += 1
    return count

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find objects
    objects = find_objects(input_grid)

    output_grid_rows = []

    # Iterate through objects
    for obj in objects:
        # Count white pixels (replication factor)
        replication_factor = count_white_pixels(input_grid, obj)

        # Get all row indices for the current object
        rows = sorted(list(set([r for r, c in obj])))

        # Replicate all rows of the object
        for row_index in rows:
            for _ in range(max(1, replication_factor)):  # Ensure at least one replication
                output_grid_rows.append(input_grid[row_index])

    # Construct output grid
    output_grid = np.array(output_grid_rows)
    return output_grid
```
