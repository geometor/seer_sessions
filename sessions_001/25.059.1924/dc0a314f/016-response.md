# dc0a314f • 016 • example_3 • investigate_coder

---
```python
"""
The transformation extracts specific colored pixels from the input grid to create a smaller output grid. The selection is based on a pattern that starts from the top-left and moves across the grid, selecting non-uniform sized sub-blocks, and is likely influenced by the color of the pixels.
"""

import numpy as np

def get_objects(grid):
    """
    Identify contiguous blocks of the same color as objects.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1]
                or visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                obj = []
                dfs(row, col, grid[row, col], obj)
                if obj:
                    objects.append(obj)
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((5, 5), dtype=int)
    # find objects in the input grid
    objects = get_objects(input_grid)
    
    # selection pattern.
    # define offsets for row and col and block sizes

    row_offsets = [0, 1, 2, 3, 4]
    col_offsets = [2, 3, 4, 4, 5]

    # extract the selected pixels
    row_idx = 0
    for i in range(len(row_offsets)):
          col_idx = 0
          for j in range(len(col_offsets)):
            output_grid[row_idx, col_idx] = input_grid[row_offsets[i], col_offsets[j]]
            col_idx +=1
          row_idx += 1

    return output_grid
```
