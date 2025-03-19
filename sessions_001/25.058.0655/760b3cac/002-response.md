# 760b3cac • 002 • example_1 • investigate_coder

---
```python
"""
Copies yellow pixels from the input grid to the output grid.
Shifts azure pixels in the top three rows of the input grid to the left in the output grid,
ensuring the leftmost azure pixel occupies the first column that previously contained azure.
"""

import numpy as np

def get_objects(grid, color):
    # Find objects of a specific color in the grid.
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] == color:
                object_pixels = []
                queue = [(r, c)]
                visited[r, c] = True

                while queue:
                    curr_r, curr_c = queue.pop(0)
                    object_pixels.append((curr_r, curr_c))

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        new_r, new_c = curr_r + dr, curr_c + dc
                        if 0 <= new_r < rows and 0 <= new_c < cols and \
                           not visited[new_r, new_c] and grid[new_r, new_c] == color:
                            queue.append((new_r, new_c))
                            visited[new_r, new_c] = True

                objects.append(object_pixels)
    return objects

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""

    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Copy yellow pixels directly.
    # No change needed as we are copying the whole input_grid

    # 2. Transform azure pixels in the top 3 rows.
    azure_objects = get_objects(input_grid, 8)
    
    # Find the leftmost column containing azure in the top 3 rows
    leftmost_col = cols
    for obj in azure_objects:
        for r, c in obj:
          if r < 3:
            leftmost_col = min(leftmost_col, c)
    
    # collect the azure pixels in the top 3 rows
    top_azure_pixels = []
    for obj in azure_objects:
      for r, c in obj:
        if r < 3:
            top_azure_pixels.append((r,c))
            output_grid[r,c] = 0 # erase

    # place azure pixels in the new location
    for r, c in top_azure_pixels:
        new_c = c - leftmost_col # shift by the difference
        output_grid[r,new_c] = 8


    return output_grid
```
