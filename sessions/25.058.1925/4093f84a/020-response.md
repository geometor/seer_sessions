# 4093f84a • 020 • refine_coder

---
```python
"""
1.  **Identify Blue Objects:** Locate all contiguous regions (objects) of blue (1) pixels in the input grid. Contiguous means connected horizontally, vertically, or diagonally.
2.  **Replace with Gray:** For *each* blue object, replace all of its pixels with gray (5) pixels in the output grid, maintaining the exact same shape and position.
3. **All Other Colors:** All other colors remain unchanged.
4. **Gray areas are Irrelevant:** the gray areas are simply the absence of any other color.
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous objects of a given color in a grid."""
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(i, j, current_object):
        """Depth-first search to find contiguous pixels."""
        if i < 0 or i >= grid.shape[0] or j < 0 or j >= grid.shape[1]:
            return
        if visited[i, j] or grid[i, j] != color:
            return

        visited[i, j] = True
        current_object.append((i, j))

        # Check all 8 neighbors (including diagonals)
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                dfs(i + di, j + dj, current_object)

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if not visited[i, j] and grid[i, j] == color:
                current_object = []
                dfs(i, j, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    """
    Transforms the input grid according to the observed rules.
    """
    output_grid = np.copy(input_grid).astype(int)

    # Find blue objects
    blue_objects = find_objects(input_grid, 1)

    # Replace blue objects with gray
    for obj in blue_objects:
        for i, j in obj:
            output_grid[i, j] = 5

    # All other colors are unchanged, so no further operations needed

    return output_grid
```

