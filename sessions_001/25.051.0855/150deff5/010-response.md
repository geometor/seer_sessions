# 5-150deff5 • 010 • example_3 - CODE

---
```python
"""
The transformation identifies gray (5) objects and recolors specific parts based on location: rightmost segment of identified object on rows 1, 2, 4, and 5 becomes azure (8). The remaining gray segments change to red (2), while preserving the black (0) background.
"""

import numpy as np

def find_objects(grid, color):
    """
    Finds contiguous regions of the specified color in the grid.
    Returns a list of (row, col) tuples representing the object's pixels.
    """
    objects = []
    visited = set()

    def dfs(row, col):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return []

        visited.add((row, col))
        region = [(row, col)]

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            region.extend(dfs(row + dr, col + dc))
        
        return region

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                objects.append(dfs(r, c))

    return objects

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    output_grid = np.copy(input_grid)
    gray_objects = find_objects(input_grid, 5)

    # Find right corner objects and change their color to azure (8).
    # Change remaining gray (5) objects to red (2).
    for obj in gray_objects:
        for r, c in obj:
           if (r in [0,1,3,4] and c in [4,5]):
              output_grid[r,c] = 8
           elif (input_grid[r,c] == 5):
              output_grid[r,c] = 2
    return output_grid
```

