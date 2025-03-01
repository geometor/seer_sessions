# fafffa47 • 029 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find all contiguous blocks of pixels of the same color in the input grid.  These are the objects. We are particularly interested in the maroon (color 9) and blue (color 1) objects.
2.  **Maroon Object:** Locate the maroon object. If no maroon object exists, the output is an empty 3x3 grid.
3.  **Output Grid:** Create a 3x3 output grid filled with black (color 0).
4. **Red Pixel Placement** If there is a maroon object, place a red pixel (color 2) in the output grid based on these rules:
    - find the leftmost column of the maroon colored object
    - find the rightmost column of the maroon colored object
    - if the object spans 2 columns, do not place a red pixel
    - if the object spans 3 columns, place the red pixel in the top left (0,0) of the output
    - if the object spans 5 columns, place the red pixel in the top center(0,1) of the output
"""

import numpy as np

def find_objects(grid):
    """
    Identifies distinct objects within a grid.  An object is a contiguous set of
    pixels of the same color.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, object_pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        object_pixels.append((row, col))
        dfs(row + 1, col, color, object_pixels)
        dfs(row - 1, col, color, object_pixels)
        dfs(row, col + 1, color, object_pixels)
        dfs(row, col - 1, color, object_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                color = grid[row, col]
                object_pixels = []
                dfs(row, col, color, object_pixels)
                if object_pixels:
                    objects.append({'color': color, 'pixels': object_pixels})
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # find objects
    objects = find_objects(input_grid)

    # find maroon object
    maroon_object = None
    for obj in objects:
      if obj['color'] == 9:
        maroon_object = obj
        break

    # If there is a maroon object determine location for red pixel
    if maroon_object:
        maroon_left = min([c for r, c in maroon_object['pixels']])
        maroon_right = max([c for r, c in maroon_object['pixels']]) + 1
        span = maroon_right - maroon_left

        if span == 3:
          output_grid[0,0] = 2 #place red pixel
        elif span == 5:
          output_grid[0,1] = 2

    return output_grid
```
