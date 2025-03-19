# 760b3cac • 008 • example_2 • investigate_coder

---
```python
"""
Identifies azure (8) colored regions in the input grid and expands them horizontally to the right,
replacing adjacent white (0) pixels. The yellow (4) colored region remains unchanged.
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous regions of the specified color."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, current_object):
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] == color and (row, col) not in visited:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find azure objects
    azure_objects = find_objects(input_grid, 8)

    # Expand azure objects to the right
    for obj in azure_objects:
        for row, col in obj:
            if col + 1 < cols and output_grid[row,col+1] == 0 :
                output_grid[row,col+1] = 8

    return output_grid
```
