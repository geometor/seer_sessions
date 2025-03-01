# a79310a0 • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule is as follows:
1. Identify Azure Objects: Locate all contiguous regions of azure (8) pixels within the input grid.
2. Preserve Shape and size: For each azure object found, copy it's shape and size to output.
3. Translate Downward: Shift red object by adding 1 to the y-coordinate (row index) of each pixel.
4. Recolor: Change the color of copied object to red (2).
5. Leave other pixels white.
"""

import numpy as np

def find_objects(grid, color):
    # Find contiguous regions of the specified color.
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_object):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
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
                objects.append(current_object)
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find azure objects
    azure_objects = find_objects(input_grid, 8)

    # Process each azure object
    for obj in azure_objects:
        # create and translate, recolor object
        for row, col in obj:
            new_row = row + 1
            if new_row < output_grid.shape[0]: # boundary check
              output_grid[new_row, col] = 2

    return output_grid
```
