```python
"""
Transform the input grid by removing the top five rows and expanding azure regions vertically downwards in the remaining grid, while preserving other colors below the removed rows.
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous regions of the specified color."""
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
                        if 0 <= new_r < rows and 0 <= new_c < cols and not visited[new_r, new_c] and grid[new_r, new_c] == color:
                            queue.append((new_r, new_c))
                            visited[new_r, new_c] = True
                objects.append(object_pixels)
    return objects

def transform(input_grid):
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Copy the lower part of the grid, preserving colors.
    for r in range(5, rows):
        for c in range(cols):
            if input_grid[r,c] != 5:
              output_grid[r, c] = input_grid[r, c]

    # Expand azure (8) downwards.
    for r in range(5, rows):
        for c in range(cols):
            if output_grid[r,c] == 8:
                for next_r in range(r + 1, rows):
                     if output_grid[next_r,c] == 0:
                        output_grid[next_r,c] = 8
                     else:
                        break
    #move azure to top
    for c in range(cols):
      for r in range(5, rows):
        if output_grid[r,c] == 8:
           first_zero_row = -1
           for r2 in range(5):
            if output_grid[r2,c] == 0:
               first_zero_row = r2
               break
           if first_zero_row != -1:
              output_grid[first_zero_row,c] = 8
              output_grid[r,c] = 0

    return output_grid
```