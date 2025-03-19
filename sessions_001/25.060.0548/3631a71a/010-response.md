# 3631a71a • 010 • example_2 • investigate_coder

---
```python
"""
The transformation rule involves a selective masking process. The input grid is analyzed, and contiguous regions of the same color are identified as objects. The white color (0) serves as the background and remains unchanged. Objects in the grid have some of their boundary pixels masked, specifically, values of '9' on object boundaries appear to be replaced. The rest of the grid seems to be copied directly from input to output.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies contiguous regions of the same color as distinct objects.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(row, col, color, obj_pixels):
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for row in range(rows):
        for col in range(cols):
            if not visited[row, col] and grid[row, col] != 0:
                obj_pixels = []
                dfs(row, col, grid[row, col], obj_pixels)
                if obj_pixels:
                    objects.append({'color': grid[row, col], 'pixels': obj_pixels})
    return objects

def get_neighbors(grid, row, col):
    """
    Returns the neighbors of a given cell, including diagonals.
    """

    rows, cols = grid.shape
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            neighbor_row, neighbor_col = row + i, col + j
            if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
               neighbors.append((neighbor_row, neighbor_col, grid[neighbor_row, neighbor_col]))
    return neighbors

def transform(input_grid):
    """
    Transforms the input grid according to the selective masking rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # Identify objects in the input grid
    objects = find_objects(input_grid)
    
    # Selective masking: Replace '9' at boundaries with surrounding color.
    for obj in objects:
      for row,col in obj['pixels']:
          if input_grid[row,col] == 9:
            neighbors = get_neighbors(input_grid, row, col)
            for r,c,color in neighbors:
              if input_grid[r,c] != 9 and input_grid[r,c] !=0: #prioritize non-background
                output_grid[row,col] = input_grid[r,c]
                break #apply change from only first neighbor
              elif input_grid[r,c] != 9:
                output_grid[row,col] = input_grid[r,c]

    return output_grid
```
