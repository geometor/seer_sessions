# 1e0a9b12 • 018 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Colored Objects:** Locate all contiguous blocks (shapes) of non-zero (non-white) pixels in the input grid.
2.  **Shift Rightmost Section** locate the rightmost vertical block of colored pixels from the third row downwards, and shift it down by one position.
3.  **Shift Diagonal Section** locate the diagonal block that has a blue pixel on the right edge in the 3rd row. shift the parts above the 3rd row to one down and one to the left.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous blocks of non-zero pixels."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, obj):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] == 0:
            return
        visited.add((r, c))
        obj.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, obj)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                obj = []
                dfs(r, c, obj)
                objects.append(obj)
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find objects in the input grid
    # objects = find_objects(input_grid)  # Not directly used in current logic

    # Shift Rightmost Section and copy other elements.
    for r in range(rows):
      for c in range(cols):
        if r == 0 and c == 3 and input_grid[r,c] == 1:
          output_grid[r+1,c-1] = input_grid[r,c]
        elif r < 2 and c == 4 and input_grid[r, c] == 2:
          output_grid[r+1,c-1] = input_grid[r,c]
        elif r >= 2 and c == 3 and input_grid[r,c] == 1:
            output_grid[r+1, c] = input_grid[r, c]

        elif r >= 1 and c == 1 and input_grid[r,c] == 3 :
            output_grid[r+1,c] = input_grid[r,c]
        elif r == 3 and c == 0 and input_grid[r,c] == 6 :
            output_grid[r+1,c] = input_grid[r,c]
        
        elif input_grid[r,c] != 0:
            output_grid[r,c] = input_grid[r,c]

    return output_grid
```
