# 264363fd • 008 • example_2 • investigate_coder

---
```python
"""
This program transforms an input grid by identifying red rectangles with green lines and yellow intersections. 
It then creates diagonal stripes where colors 3 (green) and 2 (red), 3 and 4 (yellow), or 2 and 4 are adjacent, 
prioritizing the propagation of color 3 and then color 2 within the rectangles.
"""

import numpy as np

def get_objects(grid, color):
    """
    Finds contiguous regions (objects) of a specific color in the grid.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))

        # Explore adjacent cells (including diagonals)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                dfs(r + dr, c + dc, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                if current_object:
                    objects.append(current_object)
    return objects

def transform(input_grid):
    """
    Transforms the input grid according to the observed rules.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find red (2) rectangles and other relevant objects.  We don't need to find them explicitly
    # because the striping action is based on adjacency. We do it implicitly.

    # Iterate through the grid and apply the striping rules.
    for r in range(rows):
        for c in range(cols):
            # Check for adjacencies and apply striping
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue

                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if input_grid[r, c] == 2 and input_grid[nr, nc] == 3:
                            output_grid[r,c] = 3
                        elif input_grid[r,c] == 4 and input_grid[nr,nc] == 3:
                            output_grid[r,c] = 3
                        elif input_grid[r,c] == 4 and input_grid[nr,nc] == 2:
                            output_grid[r,c] = 2
    return output_grid
```
