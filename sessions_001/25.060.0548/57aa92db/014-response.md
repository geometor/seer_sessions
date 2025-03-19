# 57aa92db • 014 • refine_coder

---
```python
"""
1.  **Identify Objects:** Locate all contiguous blocks of non-zero pixels. Each block is an object.
2.  **Check for Single-Pixel Objects in the Third Column:** Determine if an object consists of only a single pixel AND is located in the third column (index 2).
3.  **Vertical Replication:** If an object is a single pixel AND is in the third column, replicate it vertically, filling the entire column with the object's color.
4. **Preserve Other Objects:** Objects that consist of more then a single pixel, or are not in the third column should not be changed.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, color, obj):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj.append((r, c))
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and not visited[r, c]:
                obj = []
                dfs(r, c, grid[r, c], obj)
                objects.append(obj)
    return objects

def replicate_vertically(grid, obj):
    """Replicates a single-pixel object vertically if it's in the third column."""
    output_grid = np.copy(grid)
    if len(obj) == 1:
        r, c = obj[0]
        if c == 2:  # Check if the object is in the third column
           color = grid[r,c]
           # Replicate to fill the entire column
           for i in range(0, grid.shape[0]):
               output_grid[i, c] = color

    return output_grid

def transform(input_grid):
    """Transforms the input grid according to the replication rules."""
    # Find objects
    objects = find_objects(input_grid)
    # Initialize the output grid as a copy of the input.
    output_grid = np.copy(input_grid)

    # Replicate single-pixel objects vertically, but only if in the third column.
    for obj in objects:
        output_grid = replicate_vertically(output_grid, obj)

    return output_grid
```
