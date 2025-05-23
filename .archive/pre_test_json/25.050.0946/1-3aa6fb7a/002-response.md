# 1-3aa6fb7a • 002 • example_1 - CODE

---
```python
"""
The program scans the input, keeps every shape, and adds a blue pixel (color 1) in the starting top-left cell of each color 8 shape.
"""

import numpy as np

def find_objects(grid, color):
    """
    Finds and returns a list of objects of a specified color.
    Each object is a list of (row, col) tuples.
    """
    visited = set()
    objects = []

    def dfs(row, col, current_object):
        """
        Depth-First Search to find connected cells of the same color.
        """
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or (row, col) in visited
            or grid[row, col] != color
        ):
            return
        visited.add((row, col))
        current_object.append((row, col))
        # Explore adjacent cells
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and (row, col) not in visited:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def get_top_left(obj):
    """
    Return the top-left coordinate of the object
    """
    return min(obj,key=lambda x: (x[0],x[1]))
def transform(input_grid):
    """
    Transforms the input grid to generate an output grid based on L shapes.
    """
    # initialize output_grid as copy of input
    output_grid = np.copy(input_grid)

    # find objects
    objects_8 = find_objects(input_grid, 8)
    
    # change output pixels according to color 8 objects top-left corner
    for obj in objects_8:
      top_left = get_top_left(obj)
      output_grid[top_left[0],top_left[1]] = 1

    return output_grid
```
