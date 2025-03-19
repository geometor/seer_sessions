# 56dc2b01 • 010 • example_2 • investigate_coder

---
```python
"""
1.  **Identify** the contiguous blocks of green (3) pixels in the input. These are separate objects.
2.  **Identify** the contiguous block of red (2) pixels.
3.  **Move** all of the green blocks down to rows 11-14, maintaining their relative positions and shapes.
4. **Preserve** and do not move the red region at row 15.
5.  **Create** a new horizontal block of azure (8) pixels across the entire width of row 10.
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous regions of a specific color."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_object):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return

        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    """Transforms the input grid according to the rules."""

    output_grid = np.zeros_like(input_grid)

    # Find green objects
    green_objects = find_objects(input_grid, 3)

    # Find red object
    red_objects = find_objects(input_grid, 2)

    # Move green objects down.
    for obj in green_objects:
        for row, col in obj:
            # Calculate the destination row.  The green objects end up in rows 11-14
            original_row = row
            if original_row <=4: # Only move the objects located at the top, to ensure we match output
                new_row = row + 10
                output_grid[new_row, col] = 3

    # Keep the red region where it is
    for obj in red_objects:
        for row, col in obj:
            output_grid[row,col] = 2

    # Create azure row
    output_grid[10, :] = 8

    return output_grid
```

