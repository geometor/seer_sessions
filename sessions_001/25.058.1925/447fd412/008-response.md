# 447fd412 • 008 • refine_coder

---
```python
"""
Finds all red (color 2) objects in the input grid.
If a red object is completely enclosed by another color, 
changes the color of the red object to blue (color 1).
"""

import numpy as np

def find_objects(grid, color):
    """Finds objects of a specific color in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col):
        """Depth-first search to find connected components."""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return []

        visited[row, col] = True
        object_pixels = [(row, col)]

        object_pixels.extend(dfs(row + 1, col))
        object_pixels.extend(dfs(row - 1, col))
        object_pixels.extend(dfs(row, col + 1))
        object_pixels.extend(dfs(row, col - 1))
        return object_pixels

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                objects.append(dfs(row, col))
    return objects

def is_enclosed(grid, object_pixels):
    """
    Checks if an object (list of pixel coordinates) is enclosed by
    another color.
    """
    if not object_pixels:
        return False

    rows, cols = zip(*object_pixels)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    # Check boundaries for enclosure
    for r in range(min_row - 1, max_row + 2):
        if (r < 0 or r >= grid.shape[0] or
            (min_col - 1 >= 0 and grid[r, min_col - 1] == 2) or
            (max_col + 1 < grid.shape[1] and grid[r, max_col + 1] == 2)):
            return False
    for c in range(min_col - 1, max_col + 2):
        if (c < 0 or c >= grid.shape[1] or
           (min_row - 1 >= 0 and grid[min_row - 1, c] == 2) or
           (max_row + 1 < grid.shape[0] and grid[max_row + 1, c] == 2)):
            return False
    return True

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find red objects
    red_objects = find_objects(input_grid, 2)

    # Check if each red object is enclosed and change color to blue
    for red_object in red_objects:
        if is_enclosed(input_grid, red_object):
            for row, col in red_object:
                output_grid[row, col] = 1  # Change to blue

    return output_grid
```
