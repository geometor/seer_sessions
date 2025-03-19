# 41e4d17e • 010 • refine_coder

---
```python
"""
1.  Identify all distinct blue (color 1) objects in the input grid.  A distinct object is a set of contiguous blue pixels.
2.  For each blue object:
    a. Find its horizontal center (x-axis center, i.e., column index).
    b. Draw a vertical line of color 6 (magenta) across the entire height of the grid at that x-coordinate.  The blue object may be partially or completely replaced by magenta pixels.
3.  All other pixels remain unchanged.
"""

import numpy as np

def get_objects(grid, color):
    """
    Find distinct objects of a given color in a grid.
    
    Returns a list of coordinate arrays.
    """
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, current_object):
        if (row < 0 or row >= grid.shape[0] or
            col < 0 or col >= grid.shape[1] or
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
            if grid[row, col] == color and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(np.array(current_object))
    return objects

def find_center_x(coords):
    """Find the horizontal center (column index) of a set of coordinates."""
    if len(coords) == 0:
        return None
    x_coords = coords[:, 1]
    return (x_coords.min() + x_coords.max()) // 2

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # find all distinct blue objects
    blue_objects = get_objects(input_grid, 1)

    # for each blue object
    for obj in blue_objects:
        # find x center
        center_x = find_center_x(obj)

        # draw vertical line on output_grid
        for y in range(output_grid.shape[0]):
            output_grid[y, center_x] = 6

    return output_grid
```
