# d2abd087 • 014 • refine_coder

---
```python
"""
Transforms a grid by changing the color of connected gray (5) pixels to either blue (1) or red (2) based on alternating the shapes.
"""

import numpy as np

def get_objects(grid, color):
    """
    Finds connected components of a specified color in a grid.
    """
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, current_object):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return

        visited[row, col] = True
        current_object.append((row, col))
        
        # Explore 8-connectivity (including diagonals)
        for dr in [-1, -1, -1, 0, 0, 1, 1, 1]:
            for dc in [-1, 0, 1, -1, 1, -1, 0, 1]:
                dfs(row + dr, col + dc, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)

    return objects
def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = input_grid.copy()

    # Find connected components (objects) of gray pixels (color=5)
    gray_objects = get_objects(input_grid, 5)
    
    # Alternate colors for each object found
    colors = [1, 2]  # Blue and Red
    color_index = 0

    # Iterate through the found gray objects and change their color
    for obj in gray_objects:
        for row, col in obj:
            output_grid[row, col] = colors[color_index % 2]
        color_index += 1

    return output_grid
```
