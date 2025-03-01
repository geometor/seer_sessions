# 444801d8 • 010 • example_2 • investigate_coder

---
```python
"""
Identify blue regions in the input grid. For the topmost blue region, replace any non-blue, non-background color with red.
For the bottommost blue region, replace any non-blue, non-background color with green.
"""

import numpy as np

def get_objects(grid, color):
    """
    Find connected regions of a specific color.
    """
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return []

        visited[row, col] = True
        region = [(row, col)]

        region.extend(dfs(row + 1, col))
        region.extend(dfs(row - 1, col))
        region.extend(dfs(row, col + 1))
        region.extend(dfs(row, col - 1))

        return region

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                objects.append(dfs(row, col))
    return objects

def transform(input_grid):
    # Initialize output grid with the same dimensions and background color
    output_grid = np.copy(input_grid)
    
    # Find blue objects
    blue_objects = get_objects(input_grid, 1)

    # Sort blue objects by topmost row coordinate
    blue_objects.sort(key=lambda obj: min(pixel[0] for pixel in obj))

    if len(blue_objects) >= 1:
        # Topmost blue object: replace with red (2) if original is not blue (1) or background (0)
        top_blue_object = blue_objects[0]
        for row, col in top_blue_object:
             if input_grid[row,col] != 1 and input_grid[row, col] !=0 :
                 output_grid[row,col] = 2


    if len(blue_objects) >= 2:
        # Bottommost blue object, replace non-blue, non-white with Green (3)

        bottom_blue_object = blue_objects[-1]
        for row, col in bottom_blue_object:
            if input_grid[row,col] != 1 and input_grid[row, col] !=0 :
                output_grid[row, col] = 3
    

    return output_grid
```
