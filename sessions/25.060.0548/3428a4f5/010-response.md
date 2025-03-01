# 3428a4f5 • 010 • example_2 • investigate_coder

---
```python
"""
1. Remove the Yellow Row: Delete the entire row containing only yellow (4) pixels from the input grid.
2. Crop/Resize: Focus on the top-left corner and take first 6 rows.
3. Color Transformation: Change red objects that are big enough to Green. If the red object only have size 1, remove the red object, and let it be white.
"""

import numpy as np

def find_objects(grid):
    """
    Finds connected components in a grid.
    Returns a list of objects, where each object is a set of (row, col) tuples.
    """
    visited = set()
    objects = []

    def dfs(row, col, color, current_object):
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
        current_object.add((row, col))
        dfs(row + 1, col, color, current_object)
        dfs(row - 1, col, color, current_object)
        dfs(row, col + 1, color, current_object)
        dfs(row, col - 1, color, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if (row, col) not in visited and grid[row,col]!=0:
                current_object = set()
                dfs(row, col, grid[row, col], current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    # 1. Remove the Yellow Row
    grid_no_yellow = []
    for row in input_grid:
        if not all(pixel == 4 for pixel in row):
            grid_no_yellow.append(row)
    grid_no_yellow = np.array(grid_no_yellow)

    # 2. Crop/Resize: take the top 6 rows
    cropped_grid = grid_no_yellow[:6]

    # Initialize the output grid with white (0)
    output_grid = np.zeros(cropped_grid.shape, dtype=int)

    # 3. find objects and Color Transformation
    objects = find_objects(cropped_grid)
    for obj in objects:
      if cropped_grid[list(obj)[0][0], list(obj)[0][1]] == 2:
        if len(obj) > 1:
            for row, col in obj:
                output_grid[row, col] = 3
        else:
            pass #do nothing will keep color white
      elif cropped_grid[list(obj)[0][0], list(obj)[0][1]] != 0:
          for row,col in obj:
            output_grid[row, col] = cropped_grid[row, col]
    return output_grid
```
