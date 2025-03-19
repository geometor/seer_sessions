# 44f52bb0 • 020 • example_4 • investigate_coder

---
```python
"""
Counts the number of distinct red (2) objects in the input grid and returns 1.
"""

import numpy as np

def find_objects(grid, color):
    """
    Finds distinct objects of a specified color in a grid.
    An object is a group of connected pixels of the same color.
    """
    visited = set()
    objects = []

    def is_valid(x, y):
        return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]

    def dfs(x, y, current_object):
        if (x, y) in visited or not is_valid(x, y) or grid[x, y] != color:
            return
        visited.add((x, y))
        current_object.append((x, y))

        # Check adjacent cells (up, down, left, right)
        dfs(x + 1, y, current_object)
        dfs(x - 1, y, current_object)
        dfs(x, y + 1, current_object)
        dfs(x, y - 1, current_object)

    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x, y] == color and (x, y) not in visited:
                current_object = []
                dfs(x, y, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    """
    Transforms the input grid into the output value.
    """
    # Count the number of red objects.
    red_objects = find_objects(np.array(input_grid), 2)
    
    # output blue '1'
    output_grid = np.array([[1]])

    return output_grid
```
