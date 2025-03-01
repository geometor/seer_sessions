# 3428a4f5 • 014 • refine_coder

---
```python
"""
1. Remove Yellow Row: Identify and remove any row that consists entirely of yellow pixels.
2. Crop: If the grid has more than 6 rows, keep only the top 6 rows. If the grid has less than or equal to 6 rows, keep the original grid height.
3. Red objects: If there is red object and has size 1, remove it(change to white). If the red object has size greater than 1, change it to green.
4. Other color: keep the original colors.
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

    # 2. Crop/Resize: take the top 6 rows, or keep original height if <= 6
    cropped_grid = grid_no_yellow[:6]

    # 3 & 4. find objects and Color Transformation
    output_grid = np.copy(cropped_grid) # Initialize with cropped grid
    objects = find_objects(cropped_grid)

    for obj in objects:
      color = cropped_grid[list(obj)[0][0], list(obj)[0][1]]
      if color == 2: # Red Object
        if len(obj) == 1:
            for row, col in obj:
                output_grid[row, col] = 0  # Remove (change to white)
        elif len(obj) > 1:
            for row, col in obj:
                output_grid[row, col] = 3  # Change to green

    return output_grid
```

