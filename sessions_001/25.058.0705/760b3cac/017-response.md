# 760b3cac • 017 • refine_coder

---
```python
"""
1.  **Identify Objects:** Locate all contiguous regions (objects) of azure (8) and yellow (4) pixels.
2.  **Yellow Object Rule:** Yellow objects remain unchanged.
3.  **Azure Object Rule:** For each azure object:
    *   Determine the minimum (westernmost) column index occupied by the object.
    *   Extend the object westward by one column, starting from the minimum column, filling the additional column locations with azure (8).
4. Iterate through the azure pixels from top to bottom and left to right.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects in a grid.
    Returns a dictionary of objects, where keys are colors and values are lists of positions.
    """
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, color, positions):
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row, col] != color:
            return
        visited.add((row, col))
        positions.append((row, col))
        dfs(row + 1, col, color, positions)
        dfs(row - 1, col, color, positions)
        dfs(row, col + 1, color, positions)
        dfs(row, col - 1, color, positions)

    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                color = grid[row, col]
                if color != 0:
                    positions = []
                    dfs(row, col, color, positions)
                    if color not in objects:
                        objects[color] = []
                    objects[color].append(positions)
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find objects in the input grid
    objects = find_objects(input_grid)
    
    # Yellow Object Rule: Yellow objects remain unchanged
    if 4 in objects:
      for yellow_object in objects[4]:
          for row, col in yellow_object:
              output_grid[row,col] = 4

    # Azure Object Rule: Extend each azure object westward by one column
    if 8 in objects:
        for azure_object in objects[8]:
            # Determine the minimum column index
            min_col = min(pos[1] for pos in azure_object)

            # Extend westward by one column
            new_col = min_col - 1
            if new_col >= 0:
                for row, _ in azure_object:
                  output_grid[row, new_col] = 8
            
            # copy original object
            for row, col in azure_object:
                output_grid[row,col] = 8

    return output_grid
```
