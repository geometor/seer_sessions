# 1-3aa6fb7a • 006 • refine_code - CODE

---
```python
"""
1. Identify Azure Objects: Find all contiguous groups of azure (color 8) pixels.
2. Filter by Shape: From these azure objects, select only those with a 1x2 shape (1 row, 2 columns).
3. Find the Target: Among the 1x2 azure objects, locate the one that is the *lower-rightmost*.
   - Compare row indices (higher index is lower).
   - If row indices are equal, compare column indices (higher index is more to the right).
4. Split and Recolor: Split the lower-rightmost 1x2 object into two individual pixels. The left pixel is recolored blue (color 1) and the right pixel is kept azure (color 8).
5. Preserve the Rest: All other azure objects (those that are not 1x2, or are 1x2 but not the lower-rightmost) are kept as they are in the input. All other non-azure pixels stay the same.
"""

import numpy as np

def find_objects(grid, color):
    """
    Finds contiguous blocks (objects) of a specified color in the grid.
    Returns a list of bounding box coordinates, each as (min_row, min_col, max_row, max_col).
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_object):
        """Depth-First Search helper to find contiguous pixels."""
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
                if current_object:
                    min_row, min_col = np.min(current_object, axis=0)
                    max_row, max_col = np.max(current_object, axis=0)
                    objects.append((min_row, min_col, max_row, max_col))

    return objects

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid) # Start with a copy of the input
    azure_objects = find_objects(input_grid, 8)

    # Find the lower-rightmost 1x2 azure object
    lower_right_object = None
    for obj in azure_objects:
        min_row, min_col, max_row, max_col = obj
        if max_row - min_row == 0 and max_col - min_col == 1:  # Check for 1x2 shape
            if lower_right_object is None:
                lower_right_object = obj
            else:  # Find the most lower-right object
                if min_row > lower_right_object[0]:
                    lower_right_object = obj
                elif min_row == lower_right_object[0] and min_col > lower_right_object[1]:
                    lower_right_object = obj

    # Split and change the object
    if lower_right_object is not None:
        min_row, min_col, max_row, max_col = lower_right_object
        output_grid[min_row, min_col] = 1  # Change first pixel to blue
        #output_grid[max_row, max_col] = 8 #Second pixel is already azure (no change needed because of the np.copy)

    return output_grid
```
