# 99fa7670 • 018 • refine_coder

---
```python
"""
1. **Identify Objects:** Find all contiguous non-zero blocks of pixels in the input grid.
2. **Horizontal Expansion with Blocking:** For each object, expand the object's color horizontally to the right until either the edge of the grid or another object is encountered.
3. **No Vertical Expansion:** Do NOT expand objects vertically, unlike the previous, incorrect approach. The objects only expand to the right.
"""

import numpy as np

def find_objects(grid):
    """Finds all contiguous non-zero blocks of pixels and returns them as a list of (row, col, color) tuples representing the starting pixel of each object."""
    objects = []
    visited = set()

    def dfs(row, col, color):
        """Depth-first search to find contiguous blocks."""
        if (row, col) in visited or row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or grid[row, col] != color:
            return
        visited.add((row, col))
        dfs(row + 1, col, color)
        dfs(row - 1, col, color)
        dfs(row, col + 1, color)
        dfs(row, col - 1, color)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and (r, c) not in visited:
                objects.append((r, c, grid[r, c]))
                dfs(r, c, grid[r, c])  # Mark the entire object as visited.
    return objects

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    output_grid = np.zeros_like(input_grid) # Start with a blank grid
    objects = find_objects(input_grid)

    for r, c, color in objects:
        # Horizontal Expansion with Blocking
        output_grid[r,c] = color
        for c2 in range(c + 1, output_grid.shape[1]):
            if input_grid[r,c2] == 0:
                output_grid[r, c2] = color
            else:
                break # Stop expansion at the next object

    return output_grid
```
