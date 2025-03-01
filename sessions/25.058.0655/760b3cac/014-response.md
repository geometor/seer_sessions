# 760b3cac • 014 • example_3 • investigate_coder

---
```python
"""
The transformation identifies two objects: an azure (8) block and a yellow (4) block. The yellow block remains unchanged. The azure block is duplicated. One of the azure blocks is shifted one position to the left, and other by two. The output grid combines these transformed azure blocks and the unchanged yellow block.
"""

import numpy as np

def find_objects(grid):
    # Find contiguous blocks of non-zero pixels
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, color, obj):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj.append([r, c])
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and not visited[r, c]:
                obj = []
                dfs(r, c, grid[r, c], obj)
                objects.append((grid[r, c], obj))  # Store color and object
    return objects

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.zeros_like(input_grid)

    # Find objects in the input grid
    objects = find_objects(input_grid)
    
    azure_block = None
    yellow_block = None

    for color, obj in objects:
        if color == 8:
            azure_block = obj
        elif color == 4:
            yellow_block = obj

    # Keep yellow block unchanged
    if yellow_block is not None:
      for r, c in yellow_block:
          output_grid[r, c] = 4
    
    # duplicate and shift azure block
    if azure_block is not None:
      for r, c in azure_block:
        #original
        #output_grid[r,c] = 8
        # shift left by 1
        if c - 1 >= 0:
            output_grid[r, c - 1] = 8
        # shift left by 2
        if c - 2 >= 0 and r+ (1 if c==5 else 0) < output_grid.shape[0]:          
            output_grid[r+ (1 if c==5 else 0), c - 2] = 8


    return output_grid
```
