# b548a754 • 010 • example_2 • investigate_coder

---
```python
"""
1. Identify the green object and the red object it encloses.
2. Find the rightmost edge of the colored area (non-zero pixels).
3. Extend the green object horizontally to the right edge of the colored section.
4. Extend the red object horizontally, within the green object, to the same right edge.
5. Leave all other pixels as zero/white.
"""

import numpy as np

def find_objects(grid, color):
    """Find contiguous regions of a specific color."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, current_object):
        """Depth-first search to explore contiguous regions."""
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def get_bounding_box(obj):
    """Get the bounding box of a list of coordinates."""
    min_row = min(p[0] for p in obj)
    max_row = max(p[0] for p in obj)
    min_col = min(p[1] for p in obj)
    max_col = max(p[1] for p in obj)
    return min_row, max_row, min_col, max_col

def rightmost_colored_edge(grid):
    """Determine right most edge."""
    max_col = 0
    for r in range(grid.shape[0]):
      for c in range(grid.shape[1]):
        if grid[r,c] != 0:
          if c > max_col:
            max_col = c
    return max_col

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.zeros_like(input_grid)

    # Find green and red objects.
    green_objects = find_objects(input_grid, 3)
    red_objects = find_objects(input_grid, 2)
    
    # Find rightmost colored edge (excluding stray pixel)
    right_edge = rightmost_colored_edge(input_grid)


    # Extend green object.
    for green_object in green_objects:
      
        min_row, max_row, min_col, _ = get_bounding_box(green_object)

        for r in range(min_row, max_row + 1):
          for c in range(min_col,right_edge + 1):
            output_grid[r,c] = 3
            
    # Extend red object.
    for red_object in red_objects:
        min_row, max_row, min_col, _ = get_bounding_box(red_object)
        for r in range(min_row, max_row + 1):
            for c in range(min_col, right_edge + 1):
                output_grid[r, c] = 2

    return output_grid
```
