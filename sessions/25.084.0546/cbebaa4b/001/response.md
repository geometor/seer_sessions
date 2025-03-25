```python
"""
Rearrange colored objects within the grid, filling empty spaces. There's a complex interaction in the center that's handled as a special case.
"""

import numpy as np

def find_objects(grid):
    """Finds all contiguous blocks of non-zero pixels."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, color, obj):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj.append((r, c))
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c] and grid[r, c] != 0:
                obj = []
                dfs(r, c, grid[r, c], obj)
                objects.append((grid[r, c], obj))  # Store color and object pixels
    return objects

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid, then we will modify it
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Complex Center Rearrangement (rows 10-17, cols 9-16)
    center_input = input_grid[10:18, 9:17]
    color_counts = {}
    for color in range(1, 10):  # Count non-zero colors
        color_counts[color] = np.sum(center_input == color)

    center_output = output_grid[10:18, 9:17]
    idx = 0
    for c in range(center_output.shape[1]):
      for r in range(center_output.shape[0]):
        for color in range(1,10):
          if color_counts[color] > 0:
             center_output[r,c] = color
             color_counts[color] -= 1
             break


    # Move Other Objects, handling color 3 (green) first if it exists
    objects = find_objects(input_grid)
    
    colors_present = sorted(list(set([obj[0] for obj in objects])))

    #ensure 3 is at front
    if 3 in colors_present:
      colors_present.insert(0, colors_present.pop(colors_present.index(3)))

    row_idx = 0
    col_idx = 0

    for color in colors_present:
      for _, obj_pixels in [o for o in objects if o[0] == color]:
            for r, c in obj_pixels:
                # Skip the center region
                while 10 <= row_idx < 18 and 9 <= col_idx < 17:
                    col_idx += 1
                    if col_idx >= cols:
                        col_idx = 0
                        row_idx += 1
                    if row_idx >= rows:
                        break
                if row_idx >= rows:
                    break

                output_grid[row_idx, col_idx] = color
                col_idx += 1
                if col_idx >= cols:
                    col_idx = 0
                    row_idx += 1

    return output_grid
```