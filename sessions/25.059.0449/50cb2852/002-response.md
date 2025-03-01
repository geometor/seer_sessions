# 50cb2852 • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule identifies rectangular objects of uniform color (excluding white) in the input grid and adds an azure (8) colored outline, one pixel thick, inside each rectangle.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies rectangular objects of uniform color (excluding white/0) in the grid.
    Returns a list of (color, (min_row, max_row, min_col, max_col)) tuples.
    """
    objects = []
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, min_row, max_row, min_col, max_col):
        if (r, c) in visited or not is_valid(r, c) or grid[r][c] != color:
            return min_row, max_row, min_col, max_col
        visited.add((r, c))
        min_row = min(min_row, r)
        max_row = max(max_row, r)
        min_col = min(min_col, c)
        max_col = max(max_col, c)
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            min_row, max_row, min_col, max_col = dfs(r + dr, c + dc, color, min_row, max_row, min_col, max_col)
        return min_row, max_row, min_col, max_col

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0 and (r, c) not in visited:
                color = grid[r][c]
                min_row, max_row, min_col, max_col = dfs(r, c, color, rows, -1, cols, -1)
                objects.append((color, (min_row, max_row, min_col, max_col)))
    return objects

def transform(input_grid):
    """
    Transforms the input grid by adding an azure outline to each colored rectangle.
    """
    output_grid = np.copy(input_grid)
    objects = find_objects(input_grid)

    # Iterate through each identified object
    for color, (min_row, max_row, min_col, max_col) in objects:
        # create outlined inset, unless original dimension is too small
        if max_row - min_row >= 2 and max_col - min_col >=2:
          for r in range(min_row + 1, max_row):
              for c in range(min_col + 1, max_col):
                  output_grid[r][c] = 8
    
    return output_grid
```
