# 760b3cac • 002 • example_1 • investigate_coder

---
```python
"""
Preserve the yellow object, move all azure pixels to the left, and fill the first three rows.
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous blocks of a specified color in the grid."""
    visited = set()
    objects = []

    def dfs(r, c, current_object):
        """Depth-First Search to find contiguous pixels."""
        if (r, c) in visited or not (0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    # Initialize output_grid as a copy of the input_grid
    output_grid = input_grid.copy()

    # Find objects of color 4 (yellow) and 8 (azure)
    yellow_objects = find_objects(input_grid, 4)
    azure_objects = find_objects(input_grid, 8)

    # Remove all azure objects from the output grid, replace with 0
    for obj in azure_objects:
        for r, c in obj:
            output_grid[r, c] = 0

    # collect all of the 8's
    num_azure = 0
    for obj in azure_objects:
      num_azure += len(obj)

    # add the 8's to the top-left, filling in the first 3 rows
    row = 0
    col = 0

    for _ in range(num_azure):
        if row < 3:
           output_grid[row,col] = 8
           col += 1
           if col >= input_grid.shape[1]:
              col = 0
              row += 1

    return output_grid
```
