# 760b3cac • 010 • refine_coder

---
```python
"""
The transformation rule extends an azure shape to the right edge of the grid if a green object is present in the same row and the green object touches the right edge.
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

def object_touches_right_edge(grid, obj):
    """Checks if an object touches the right edge of the grid."""
    _, cols = grid.shape
    for _, c in obj:
        if c == cols - 1:
            return True
    return False

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find azure objects
    azure_objects = find_objects(input_grid, 8)
    
    # Find green objects
    green_objects = find_objects(input_grid, 3)

    # Conditional Extension to Right
    for azure_obj in azure_objects:
        # Get the row indices of the azure object
        azure_row_indices = set([r for r, _ in azure_obj])

        extend_row = False
        for green_obj in green_objects:
           if object_touches_right_edge(input_grid, green_obj):
                green_row_indices = set([r for r,_ in green_obj])
                if len(azure_row_indices.intersection(green_row_indices)) > 0:
                    extend_row = True
                    break
        
        if extend_row:
            for r in azure_row_indices:
                 # Find the rightmost azure pixel in the current row
                rightmost_col = max(c for row, c in azure_obj if row == r)
                
                #fill pixels from rightmost to edge
                for c in range(rightmost_col + 1, cols):
                    output_grid[r,c] = 8

    return output_grid
```
