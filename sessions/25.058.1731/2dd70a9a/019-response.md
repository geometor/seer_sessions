# 2dd70a9a • 019 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find all contiguous regions (objects) of green (3) and red (2) pixels in the input grid.
2.  **Horizontal Expansion:** For each green and red object:
    *   Expand the object horizontally to the left and right.
    *   During expansion, overwrite pixels that are white (0) or matching color of the expanding object.
    *   Stop expansion in a given direction if an azure (8) pixel is encountered,
        or the edge of the grid.
    *   If an object is surrounded on both the left and right by an azure (8)
        pixel, do not expand
"""

import numpy as np

def get_objects(grid, colors):
    """Find contiguous regions of specified colors."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(row, col, color, current_object):
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, color, current_object)
        dfs(row - 1, col, color, current_object)
        dfs(row, col + 1, col, current_object)
        dfs(row, col - 1, col, current_object)

    for row in range(rows):
        for col in range(cols):
            if not visited[row, col] and grid[row, col] in colors:
                current_object = []
                dfs(row, col, grid[row, col], current_object)
                objects.append((grid[row,col], current_object))  # Store color with object
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Identify target objects (green and red regions)
    target_objects = get_objects(input_grid, [3, 2])

    # Horizontal expansion for each object
    for color, object_pixels in target_objects:
        # find object extents
        min_col = min(col for _, col in object_pixels)
        max_col = max(col for _, col in object_pixels)

        # check for blocking azure pixels on both sides
        blocked_left = False
        blocked_right = False

        #check same row
        for row, _ in object_pixels:
            if min_col > 0 and input_grid[row, min_col - 1] == 8:
                blocked_left = True
            if max_col < cols - 1 and input_grid[row, max_col + 1] == 8:
                blocked_right = True
            if blocked_left and blocked_right:
              break

        if blocked_left and blocked_right:
             continue # skip expansion for this object

        for row, col in object_pixels:

            # Expand to the left
            c = col - 1
            while c >= 0:
                if input_grid[row, c] == 8:
                    break
                if output_grid[row,c] == 0 or output_grid[row,c] == color:
                   output_grid[row, c] = color
                else:
                    break
                c -= 1

            # Expand to the right
            c = col + 1
            while c < cols:
                if input_grid[row, c] == 8:
                    break

                if output_grid[row,c] == 0 or output_grid[row,c] == color:
                   output_grid[row, c] = color
                else:
                    break
                c += 1

    return output_grid
```
