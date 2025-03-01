# 447fd412 • 004 • example_1 • investigate_coder

---
```python
"""
Identifies a blue shape and two red squares in the input grid.
Copies the blue shape to the output grid.
Expands the red squares, connecting them with blue, 
and forming a larger shape that includes the original blue shape.
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

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find blue and red objects
    blue_objects = find_objects(input_grid, 1)
    red_objects = find_objects(input_grid, 2)

    # Find the bounding box of each 2x2 red square and expand
    for red_object in red_objects:
      if len(red_object) == 4:  # Ensure we only consider 2x2 initially
        min_row = min(r for r, c in red_object)
        max_row = max(r for r, c in red_object)
        min_col = min(c for r, c in red_object)
        max_col = max(c for r, c in red_object)

        # add the blue (1) between the red blocks
        for r in range(min_row, input_grid.shape[0]):
            for c in range(input_grid.shape[1]):
                if input_grid[r,c] == 0:
                    output_grid[r,c] = 1

    return output_grid
```
