# d5d6de2d • 008 • refine_coder

---
```python
"""
1.  **Find Red Objects:** Identify all distinct contiguous regions of red (color 2) pixels in the input grid.
2.  **Count and Sort:** Count the number of red objects found and sort them from top to bottom based on the row of the object.
3. **Transformation Rules**
    *   The top-most object is replaced by a single green (color 3) pixel in the top-left corner of its bounding box.
    *   The second top-most object (if present) is replaced by a single green (color 3) pixel at the top-left corner of its bounding box.
    *   The third top-most object (if present) is replaced by a 2x2 green block of pixels at the top-left corner of its bounding box.
    *   If there are more than 3 red objects, apply the rule for the third object to the all remaining objects.
4.  **Background:** All non-red pixels in the input grid should remain black (color 0) in the output grid.
"""

import numpy as np

def find_objects(grid, color):
    """Finds connected regions of the specified color."""
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

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

def get_bounding_box(obj):
    """Calculates the bounding box of an object."""
    min_row = min(pixel[0] for pixel in obj)
    max_row = max(pixel[0] for pixel in obj)
    min_col = min(pixel[1] for pixel in obj)
    max_col = max(pixel[1] for pixel in obj)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # find red objects
    red_objects = find_objects(input_grid, 2)
    
    # sort objects based on top-most row (y-coordinate)
    red_objects.sort(key=lambda obj: min(pixel[0] for pixel in obj))

    # change output pixels based on shape abstraction rules
    for i, obj in enumerate(red_objects):
        top_left, _ = get_bounding_box(obj)
        if i < 2:
            # First two objects become single points
            output_grid[top_left[0], top_left[1]] = 3
        else:
            # Third and subsequent objects become 2x2 blocks
            output_grid[top_left[0], top_left[1]] = 3
            output_grid[top_left[0], top_left[1] + 1] = 3
            output_grid[top_left[0] + 1, top_left[1]] = 3
            output_grid[top_left[0] + 1, top_left[1] + 1] = 3

    return output_grid
```
