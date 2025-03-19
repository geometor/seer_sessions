# 760b3cac • 008 • example_2 • investigate_coder

---
```python
"""
The transformation rule extends an azure shape to the right edge of the grid.
"""

import numpy as np

def find_objects(grid, color):
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(r, c, current_object):
        if (r < 0 or r >= rows or c < 0 or c >= cols or visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find azure objects
    azure_objects = find_objects(input_grid, 8)

    # Extend azure objects to the right
    for obj in azure_objects:
        # Check if the object touches the second to last column
        touches_second_to_last_column = any(c == cols - 4 for _, c in obj) # 5 in zero index is cols-4
        if touches_second_to_last_column:
            # Get the row indices of the object
            row_indices = [r for r, _ in obj]
            for r in row_indices:
                # Find the rightmost azure pixel in the current row
                rightmost_col = max(c for row, c in obj if row == r)
                
                #fill pixels from rightmost to edge
                for c in range(rightmost_col + 1, cols):
                    output_grid[r,c] = 8
                
    return output_grid
```
