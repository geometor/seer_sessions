# 0e206a2e • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule involves identifying contiguous blocks of non-zero colored pixels (objects) in the input grid and moving them to the bottom-right corner of the output grid. The objects maintain their relative positions when possible and sometimes expand, merging with adjacent objects. The remaining cells in the output grid are filled with zeros.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous blocks of non-zero colored pixels in the grid.
    Returns a list of objects, where each object is a list of (row, col) coordinates.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, current_object):
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row, col] == 0:
            return
        visited.add((row, col))
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    """
    Transforms the input grid according to the identified rule.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    objects = find_objects(input_grid)

    # Calculate total bounding box of all objects
    min_row = rows
    min_col = cols
    max_row = 0
    max_col = 0

    for obj in objects:
        for r, c in obj:
            min_row = min(min_row, r)
            min_col = min(min_col, c)
            max_row = max(max_row, r)
            max_col = max(max_col, c)
    
    total_height = max_row - min_row + 1
    total_width = max_col - min_col + 1

    # Calculate starting position in output grid (bottom-right corner)
    start_row = rows - total_height
    start_col = cols - total_width
    
    # Move objects into the output grid
    for obj in objects:
      for r,c in obj:
        output_grid[r - min_row + start_row, c-min_col + start_col] = input_grid[r,c]


    return output_grid.tolist()
```
