# 29c11459 • 008 • refine_coder

---
```python
"""
1.  **Identify Objects:** Locate all contiguous regions of non-zero pixels. Each region is an object, characterized by its color and the set of its pixel coordinates.

2.  **Determine Expansion Direction:**
    *   If an object is alone on a row, check if its color appears expanded horizontally in the corresponding output row. If so, replicate the color across the output row in both directions to fill the row from the object's position to the edges of the grid.

3. **Apply expansion to edges.**
   *  If multiple objects are present in a single row, expand each object to the left or right edges of the output row.

4.  **Combine Results:** if multiple rules apply, combine the transformed pixels to the output grid
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous regions of non-zero pixels (objects)."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, color, object_pixels):
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row, col] != color:
            return
        visited.add((row, col))
        object_pixels.append((row, col))
        dfs(row + 1, col, color, object_pixels)
        dfs(row - 1, col, color, object_pixels)
        dfs(row, col + 1, color, object_pixels)
        dfs(row, col - 1, color, object_pixels)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] != 0 and (row, col) not in visited:
                object_pixels = []
                dfs(row, col, grid[row, col], object_pixels)
                objects.append({'color': grid[row, col], 'pixels': object_pixels})
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find objects
    objects = find_objects(input_grid)

    # Apply expansion logic
    for obj in objects:
        color = obj['color']
        pixels = obj['pixels']
        object_rows = {r for r, _ in pixels}

        for row in object_rows:
            # Expand to edges
            min_col = 0
            max_col = cols - 1

            #find object position
            object_cols = []
            for r,c in pixels:
                if r == row:
                    object_cols.append(c)
            
            min_obj_col = min(object_cols)
            max_obj_col = max(object_cols)

            for col in range(min_col, min_obj_col + 1):
                output_grid[row, col] = color  # left expansion
            for col in range(max_obj_col, max_col+ 1):
                output_grid[row, col] = color # right expansion

    return output_grid
```
