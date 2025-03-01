# 9edfc990 • 020 • refine_coder

---
```python
"""
1.  **Identify the First Row Colors:** Determine the set of unique colors present in the first row of the input grid.
2.  **Identify Objects:** Identify all contiguous regions (objects) of the same color within the input grid.
3.  **Determine Background:** For each object, identify the color(s) of any adjacent pixel that is a different color. This is considered the background color.
4.  **Fill Objects:** For each identified object:
    - If an objects color is different than a background color
    - Then, if any background color is present in the first row, change *all* pixels in the object to that color. If multiple background colors exist, only one will be in the first row.
5.  **Output:** Return the modified grid.
"""

import numpy as np

def get_first_row_colors(grid):
    """Returns a set of unique colors present in the first row of the grid."""
    return set(grid[0])

def find_objects(grid):
    """
    Identifies distinct objects in the grid.
    An object is a group of connected pixels of the same color.
    """
    objects = {}
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, object_id):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        objects[object_id].append((row, col))
        dfs(row + 1, col, color, object_id)
        dfs(row - 1, col, color, object_id)
        dfs(row, col + 1, color, object_id)
        dfs(row, col - 1, color, object_id)

    object_count = 0
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                color = grid[row, col]
                object_id = f"object_{object_count}"
                objects[object_id] = []
                dfs(row, col, color, object_id)
                object_count += 1
    return objects

def get_background_colors(grid, object_pixels):
    """
    Finds the set of unique background colors adjacent to an object.
    """
    background_colors = set()
    object_color = grid[object_pixels[0]] # all pixels in object will be same

    for row, col in object_pixels:
        # Check adjacent pixels (up, down, left, right)
        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        for n_row, n_col in neighbors:
            if 0 <= n_row < grid.shape[0] and 0 <= n_col < grid.shape[1]:
                if grid[n_row, n_col] != object_color:
                    background_colors.add(grid[n_row, n_col])
    return background_colors

def transform(input_grid, output_grid=None): # added output for testing
    # initialize output_grid
    output_grid_copy = np.copy(input_grid)

    # 1. Identify First Row Colors
    first_row_colors = get_first_row_colors(input_grid)

    # 2. Identify Objects
    objects = find_objects(input_grid)

    # 3 & 4. Determine Background and Fill Objects
    for object_id, pixels in objects.items():
        object_color = input_grid[pixels[0]]
        background_colors = get_background_colors(input_grid, pixels)

        # find the background color that is also in first row
        fill_color = None
        for bg_color in background_colors:
            if bg_color in first_row_colors:
                fill_color = bg_color
                break

        # fill if valid
        if fill_color is not None:
          for row, col in pixels:
              output_grid_copy[row, col] = fill_color

    return output_grid_copy
```
