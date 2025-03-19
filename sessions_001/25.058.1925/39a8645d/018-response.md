# 39a8645d • 018 • example_3 • investigate_coder

---
```python
"""
Identifies and extracts the azure object located in the top-left quadrant of the input grid, 
then places it centered within a 3x3 output grid.
"""

import numpy as np

def find_objects(grid):
    """
    Finds all distinct objects in a grid.
    Returns a dictionary of objects, keyed by color, 
    with each entry containing a list of coordinates.
    """
    objects = {}
    visited = set()

    def dfs(row, col, color, coords):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        coords.append((row, col))
        dfs(row + 1, col, color, coords)
        dfs(row - 1, col, color, coords)
        dfs(row, col + 1, color, coords)
        dfs(row, col - 1, color, coords)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            color = grid[row, col]
            if color != 0 and (row, col) not in visited:
                if color not in objects:
                    objects[color] = []
                coords = []
                dfs(row, col, color, coords)
                objects[color].append(coords)
    return objects

def find_top_left_object(objects, color):
    """Finds the object of the specified color closest to the top-left."""
    if color not in objects:
        return None

    min_row = float('inf')
    min_col = float('inf')
    target_object = None

    for obj_coords in objects[color]:
        for row, col in obj_coords:
            if row < min_row or (row == min_row and col < min_col):
                min_row = row
                min_col = col
                target_object = obj_coords
    return target_object

def transform(input_grid):
    """
    Transforms the input grid by extracting the top-left azure object and placing it in a 3x3 output grid.
    """
    # Find all objects in the grid.
    objects = find_objects(input_grid)

    # Select the top-left azure object.
    target_object = find_top_left_object(objects, 8)

    # Create a 3x3 output grid filled with white.
    output_grid = np.zeros((3, 3), dtype=int)
    
    if target_object:
      # find the center of object and shift to center of 3x3
      rows = [r for r, c in target_object]
      cols = [c for r, c in target_object]
      center_row = (min(rows) + max(rows)) // 2
      center_col = (min(cols) + max(cols)) // 2

      row_shift = 1 - center_row
      col_shift = 1 - center_col

      # copy object into new grid with shift
      for r, c in target_object:
        new_r = r + row_shift
        new_c = c + col_shift
        
        if 0 <= new_r < 3 and 0 <= new_c < 3:
          output_grid[new_r, new_c] = 8

    return output_grid
```
