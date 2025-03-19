# 760b3cac • 014 • example_3 • investigate_coder

---
```python
"""
The transformation rule is as follows:
1. Identify the contiguous blocks of azure (8) and yellow (4) pixels.
2. Keep the yellow (4) pixels unchanged in the output grid.
3. Shift the azure (8) object one column to the left and duplicate it.
4. Maintain relative vertical positioning; the azure cluster remains above the yellow one.
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
    """
    Transforms the input grid according to the described rule.
    """
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find objects
    objects = find_objects(input_grid)

    # change output pixels - Preserve Yellow
    if 4 in objects:
        for yellow_object in objects[4]:
          for row, col in yellow_object:
              output_grid[row, col] = 4

    # Transform Azure: shift and duplicate
    if 8 in objects:
        for azure_object in objects[8]:
            # calculate shift
            min_col = min(pos[1] for pos in azure_object)
            
            # Original shape shifted by one column
            for row, col in azure_object:
                new_col = col -1
                if new_col >= 0:
                  output_grid[row,new_col] = 8
                
            # Duplicate the original shape
            # Find leftmost points
            leftmost_points = sorted([pos for pos in azure_object if pos[1] == min_col], key = lambda x: x[0])
            
            for point in leftmost_points:
              for row, col in azure_object:
                  
                  shifted_row = row + (point[0] - azure_object[0][0])
                  shifted_col = col + (point[1] - azure_object[0][1])

                  if 0 <= shifted_row < rows and 0 <= shifted_col < cols :

                    output_grid[shifted_row,shifted_col]=8


    return output_grid
```
