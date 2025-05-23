# 1-3aa6fb7a • 002 • example_1 - CODE

---
```python
"""
For each azure object in the input grid:
    Locate the top-left corner of the object.
    Move one cell to the right of the top-left corner.
    Change the color of this cell to blue (1).
    Preserve the initial objects.
"""

import numpy as np

def find_objects(grid, color):
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_object):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] == color:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def find_top_left(obj):
    min_row, min_col = float('inf'), float('inf')
    for row, col in obj:
        min_row = min(min_row, row)
        min_col = min(min_col, col)
    return min_row, min_col

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    
    # Find all azure (color 8) objects
    azure_objects = find_objects(input_grid, 8)
    
    # For each azure object
    for obj in azure_objects:
        # Find the top-left corner
        top_left_row, top_left_col = find_top_left(obj)
        
        # Move one cell to the right
        new_col = top_left_col + 1
        
        # Check boundaries and change the color to blue (1)
        if new_col < output_grid.shape[1]:
            output_grid[top_left_row, new_col] = 1
    
    return output_grid
```

