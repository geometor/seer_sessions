# 27a28665 • 014 • example_3 • investigate_coder

---
```python
"""
1. **Identify Objects:** Find all contiguous regions (objects) of pixels with the same color within the input grid.
2. **Filter Objects by color:** Select objects colored gray (5).
3. **Check Object Location**: Check if any part of the object touches the outer edge/border of the grid.
4. **Count Edge Objects:** Count the number of objects from step 3 (grey object touching the edge).
5. **Output:** The output is the final count. In this example, there are two grey objects on corners - all corner objects touch the edge.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous regions (objects) of the same color in a grid."""
    visited = set()
    objects = []

    def dfs(row, col, color, obj):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if (row, col) not in visited:
                obj = []
                dfs(row, col, grid[row, col], obj)
                if obj:
                    objects.append(obj)
    return objects

def is_on_edge(grid, object_pixels):
    """Checks if any pixel of an object is on the edge of the grid."""
    rows, cols = grid.shape
    for r, c in object_pixels:
        if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
            return True
    return False

def transform(input_grid):
    # Convert input to numpy array
    grid = np.array(input_grid)

    # Find all objects in the grid
    objects = find_objects(grid)

    # Filter for gray (5) objects
    gray_objects = [obj for obj in objects if grid[obj[0][0], obj[0][1]] == 5]
    
    # Count gray objects touching the edge
    count = 0
    for obj in gray_objects:
        if is_on_edge(grid, obj):
            count += 1

    return count
```
