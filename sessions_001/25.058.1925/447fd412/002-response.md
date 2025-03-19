# 447fd412 • 002 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Objects:** Locate all contiguous blue (1) and red (2) shapes in the input grid.
2.  **Red Shape Extension**: extend the red shape by converting all the white pixels that share and edge to a red pixel into a 1 (blue) pixel.
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous objects of a specific color in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(row, col, current_object):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] == color and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find red objects
    red_objects = find_objects(input_grid, 2)
    
    # Extend red objects with blue pixels
    for red_object in red_objects:
       for r,c in red_object:
           #check neighbors
           neighbors = [(r-1,c), (r+1, c), (r, c-1), (r, c+1)]
           for nr, nc in neighbors:
               if 0 <= nr < rows and 0 <= nc < cols and input_grid[nr,nc] == 0:
                   output_grid[nr,nc] = 1

    return output_grid
```
