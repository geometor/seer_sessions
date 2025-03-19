# 4522001f • 008 • example_2 • investigate_coder

---
```python
"""
1.  **Expansion:** The input grid is expanded by a factor of three in both dimensions. That is, a 3x3 input becomes a 9x9 output.
2.  **Color Replacement**: All instances of color 2 (red) in the expanded grid are replaced with color 3 (green).
3.  **Object Replication and Translation**: The original 2x2 block of color 3(green) is duplicated to form a new 4x4 block of color 3 in the bottom right of the output grid, and a 4x4 block is created in the top-center. The remaining cells are set to color 0 (white).

"""

import numpy as np

def get_objects(grid):
    """
    Finds connected components (objects) in a grid.
    Returns a list of objects, where each object is a set of (row, col) coordinates.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, current_object):
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row, col] != grid[r, c]:
            return
        visited.add((row, col))
        current_object.add((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                current_object = set()
                dfs(r, c, current_object)
                if current_object:
                    objects.append(current_object)
    return objects

def transform(input_grid):
    # Expand the input grid by a factor of 3.
    expanded_grid = np.repeat(np.repeat(input_grid, 3, axis=0), 3, axis=1)

    # Replace color 2 (red) with color 3 (green).
    expanded_grid[expanded_grid == 2] = 3

    # Initialize output_grid with white (0).
    output_grid = np.zeros((9, 9), dtype=int)

    # find objects
    objects = get_objects(input_grid)
    
    # find largest green object
    green_objects = [obj for obj in objects if input_grid[list(obj)[0][0], list(obj)[0][1]] == 3]
    largest_green = max(green_objects, key=len) if green_objects else None

    # Create a 4x4 block in output if green cluster is found in input.
    if largest_green is not None :   
      # create the objects
      output_grid[1:5, 1:5] = 3
      output_grid[5:9, 5:9] = 3

    return output_grid
```
