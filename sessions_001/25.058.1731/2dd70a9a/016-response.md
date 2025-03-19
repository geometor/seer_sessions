# 2dd70a9a • 016 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Target Objects:** Locate all contiguous regions of green (3) and red (2) pixels.
2.  **Horizontal Expansion:** For each target object (green and red regions), expand the region horizontally to the left and right.
3.  **Boundary Condition:** Stop the expansion when an azure (8) pixel or the edge of the grid is encountered.
4. **Green and red objects do not expand past each other**: The first object encountered will stop the other from expanding beyond it.
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
        dfs(row, col + 1, color, current_object)
        dfs(row, col - 1, color, current_object)

    for row in range(rows):
        for col in range(cols):
            if not visited[row, col] and grid[row, col] in colors:
                current_object = []
                dfs(row, col, grid[row, col], current_object)
                objects.append((grid[row,col], current_object))  # Store color with object
    return objects

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Identify target objects (green and red regions)
    target_objects = get_objects(input_grid, [3, 2])

    # Horizontal expansion for each object
    for color, object_pixels in target_objects:
        for row, col in object_pixels:
            # Expand to the left
            c = col - 1
            while c >= 0 and input_grid[row, c] != 8:
                if output_grid[row,c] == 0 or output_grid[row,c] == color:
                   output_grid[row, c] = color
                else:
                    break
                c -= 1
            
            # Expand to the right
            c = col + 1
            while c < cols and input_grid[row, c] != 8:
                if output_grid[row,c] == 0 or output_grid[row,c] == color:
                   output_grid[row, c] = color
                else:
                    break
                c += 1

    return output_grid
```
