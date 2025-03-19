# 39e1d7f9 • 016 • example_3 • investigate_coder

---
```python
"""
The input grid is divided into frames by vertical azure (8) columns and horizontal azure rows.
Within each frame, identify any 3x3 blocks of yellow (4) or red (2).
Consider sets of colors that are not azure (8). Within each vertical set of frames, there are blocks that start with red (2) and yellow(4). Swap those colors, such that anything that was yellow becomes red and anything red becomes yellow. The frames themselves remain unchanged.
"""

import numpy as np

def find_objects(grid, color):
    # Find contiguous regions of the specified color
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                obj_coords = []
                queue = [(r, c)]
                visited[r, c] = True

                while queue:
                    curr_r, curr_c = queue.pop(0)
                    obj_coords.append((curr_r, curr_c))

                    # Check neighbors (up, down, left, right)
                    neighbors = []
                    if curr_r > 0: neighbors.append((curr_r - 1, curr_c))
                    if curr_r < rows - 1: neighbors.append((curr_r + 1, curr_c))
                    if curr_c > 0: neighbors.append((curr_r, curr_c - 1))
                    if curr_c < cols - 1: neighbors.append((curr_r, curr_c + 1))
                    
                    for nr, nc in neighbors:
                        if grid[nr, nc] == color and not visited[nr, nc]:
                            queue.append((nr, nc))
                            visited[nr, nc] = True

                objects.append(obj_coords)

    return objects
    

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    rows, cols = input_grid.shape

    # Swap red and yellow within each frame
    for r in range(rows):
        for c in range(cols):
          if output_grid[r,c] == 2:
            output_grid[r,c] = 4
          elif output_grid[r,c] == 4:
            output_grid[r,c] = 2

    return output_grid
```
