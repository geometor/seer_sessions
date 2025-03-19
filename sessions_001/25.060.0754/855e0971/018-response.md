# 855e0971 • 018 • refine_coder

---
```python
"""
1.  **Identify Objects:** Divide the input grid into distinct objects. An object is a contiguous block of pixels of the same color.
2.  **Find White Pixels:** Locate all white pixels within each object.
3.  **Determine Replication Factor:** For each object, the replication factor is the number of white pixels within that object.
4. **Replicate Rows:** For each object, replicate each row that contains white pixels within that object. The number of times a row is replicated equals to the replication factor.
5.  **Construct the final output:** Recombine all objects in their original order, including the replicated rows.
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

def find_white_pixels_in_object(grid, object_coords):
    # Find coordinates of white pixels within a specific object.
    white_pixels = []
    for r, c in object_coords:
        if grid[r, c] == 0:
            white_pixels.append((r, c))
    return white_pixels

def transform(input_grid):
    input_grid = np.array(input_grid)
    objects = find_objects(input_grid)
    output_grid_rows = []
    processed_rows = set()

    for obj in objects:
        white_pixels = find_white_pixels_in_object(input_grid, obj)
        replication_factor = len(white_pixels)
        rows_to_replicate = {coord[0] for coord in white_pixels}

        # Add rows of the current object to output_grid_rows
        for row_index in sorted(list({coord[0] for coord in obj})): #ensure correct order
            if row_index in rows_to_replicate:
                for _ in range(replication_factor):
                    output_grid_rows.append(input_grid[row_index])
            elif row_index not in processed_rows:
                output_grid_rows.append(input_grid[row_index])
            processed_rows.add(row_index)


    output_grid = np.array(output_grid_rows)
    return output_grid
```
