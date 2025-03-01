# 6c434453 • 014 • example_2 • investigate_coder

---
```python
"""
1.  **Identify** all contiguous blue (1) regions (objects) in the input grid.
2.  **Locate** two distinct groups:
    * Group 1: the blue shapes in the top left corner
    * Group 2: the three blue lines next to each other on the left
3. **Transform as follows:**
     *  Group 1: shift the blue object down one row and left one column and change the color to red.
     * Group 2: Shift the blue object up one row and to the right one column, change the color to red.
4. All other pixels are unchanged.
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous regions of the specified color in the grid."""
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, current_object):
        """Depth-first search to find contiguous pixels."""
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
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

def move_object(object_pixels, row_shift, col_shift):
    """Shifts the object pixels by the specified row and column offsets."""
    moved_pixels = []
    for row, col in object_pixels:
        moved_pixels.append((row + row_shift, col + col_shift))
    return moved_pixels

def transform(input_grid):
    # Initialize output_grid with the same values as the input_grid
    output_grid = np.copy(input_grid)
    
    # Find all blue objects
    blue_objects = find_objects(input_grid, 1)

    # Identify the two groups based on location.
    # Assuming the top-left object is always group 1 and the middle-left is group 2
    group1 = []
    group2 = []

    for obj in blue_objects:
      if any(r < 3 for r,c in obj) and any(c < 4 for r,c in obj):
        group1 = obj
      elif any(r > 3 for r, c in obj) and any(c < 4 for r, c in obj):
        group2 = obj
    
    # Transform Group 1: shift down one row, left one column, and change to red
    if (len(group1) > 0):
      moved_group1 = move_object(group1, 1, -1)
      for row, col in moved_group1:
          if 0 <= row < output_grid.shape[0] and 0 <= col < output_grid.shape[1]:
              output_grid[row, col] = 2

    # Transform Group 2: shift up one row, right one column, and change to red
    if (len(group2) > 0):
        moved_group2 = move_object(group2, -1, 1)
        for row, col in moved_group2:
            if 0 <= row < output_grid.shape[0] and 0 <= col < output_grid.shape[1]:
                output_grid[row, col] = 2
    return output_grid
```
