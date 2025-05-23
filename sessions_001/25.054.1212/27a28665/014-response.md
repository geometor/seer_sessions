# 27a28665 • 014 • example_3 • investigate_coder

---
```python
"""
1. **Identify Objects:** The input is a 3x3 grid. Each contiguous block of the same color is one distinct object.
2.  **Count Distinct White Objects:** Count the number of distinct white (0) objects.
3.  **Output:** The output is the count of the distinct white objects. The output will always use color red.
"""

import numpy as np

def find_objects(grid, color):
    """
    Finds distinct objects of a specified color in a grid.
    An object is a group of contiguous cells of the same color.
    """
    visited = set()
    objects = []

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))

        # Explore adjacent cells (up, down, left, right)
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
    """
    Transforms the input grid to count the distinct white objects
    """
    # Find distinct white objects
    white_objects = find_objects(np.array(input_grid), 0)

    # Count the number of distinct white objects
    count = len(white_objects)
    
    # the output grid will be 1 x 1 with value of the 'count'
    output_grid = np.array([[count]])
    
    return output_grid
```
