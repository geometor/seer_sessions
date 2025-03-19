# 5521c0d9 • 004 • example_1 • investigate_coder

---
```python
"""
Shifts colored rectangular blocks upwards by a fixed number of rows, removing any rows fully occupied by white space, with special handling for overlapping blue and red blocks.
"""

import numpy as np

def find_objects(grid):
    """
    Finds distinct colored rectangular blocks in the grid.

    Args:
        grid: A 2D numpy array representing the grid.

    Returns:
        A dictionary where keys are colors and values are (min_row, max_row, min_col, max_col) tuples.
    """
    objects = {}
    visited = set()

    def dfs(row, col, color, min_row, max_row, min_col, max_col):
        if (row, col) in visited or row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or grid[row, col] != color:
            return min_row, max_row, min_col, max_col

        visited.add((row, col))
        min_row = min(min_row, row)
        max_row = max(max_row, row)
        min_col = min(min_col, col)
        max_col = max(max_col, col)

        min_row, max_row, min_col, max_col = dfs(row + 1, col, color, min_row, max_row, min_col, max_col)
        min_row, max_row, min_col, max_col = dfs(row - 1, col, color, min_row, max_row, min_col, max_col)
        min_row, max_row, min_col, max_col = dfs(row, col + 1, color, min_row, max_row, min_col, max_col)
        min_row, max_row, min_col, max_col = dfs(row, col - 1, color, min_row, max_row, min_col, max_col)
        return min_row, max_row, min_col, max_col

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            color = grid[row, col]
            if color != 0 and (row, col) not in visited:
                min_row, max_row, min_col, max_col = dfs(row, col, color, row, row, col, col)
                if color not in objects:
                    objects[color] = []
                objects[color].append((min_row, max_row, min_col, max_col))

    return objects

def transform(input_grid):
    """
    Transforms the input grid according to the described rules.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    objects = find_objects(input_grid)
    shift_amount = 4

    for color, object_list in objects.items():
      for min_row, max_row, min_col, max_col in object_list:
        new_min_row = min_row - shift_amount
        new_max_row = max_row - shift_amount

        # Handle boundary conditions and create the shifted block
        if new_min_row < 0:
            height = new_max_row + 1
            new_min_row = 0
        else:
            height = new_max_row - new_min_row + 1
        if new_max_row >=0:
          for i in range(height):
              for j in range(min_col, max_col + 1):
                  output_grid[new_min_row+i,j]=color

    return output_grid
```
