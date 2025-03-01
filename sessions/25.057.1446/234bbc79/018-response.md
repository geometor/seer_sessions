# 234bbc79 • 018 • refine_coder

---
```python
"""
1. **Identify Objects:** Find all contiguous blocks of pixels with the same color.
2. **Gray Transformation:** Change all gray (5) objects to azure (8).
3. **Azure Transformation:** An azure (8) pixel changes to magenta (6) if and only if it is *immediately* to the right of an azure pixel that *used to be* gray (5) in the input.
4. **All other pixels:** Pixels which do not meet the above criteria do not change.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects of the same color in a grid.
    Returns a list of objects, where each object is a list of (row, col) tuples.
    """
    visited = set()
    objects = []

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, color, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if (r, c) not in visited:
                current_object = []
                dfs(r, c, grid[r, c], current_object)
                if current_object:
                    objects.append(current_object)
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    objects = find_objects(input_grid)

    # Gray Transformation: Change all Gray (5) to Azure (8)
    for obj in objects:
      first_pixel_r, first_pixel_c = obj[0]
      if input_grid[first_pixel_r, first_pixel_c] == 5:
        for r, c in obj:
            output_grid[r, c] = 8

    # Azure Transformation: Azure (8) to Magenta (6) if immediately to the right of a former Gray (now Azure)
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if output_grid[r, c] == 8:  # Check each Azure pixel
                if c > 0 and input_grid[r, c-1] == 5:  # Check immediate left neighbor in *input*
                    output_grid[r, c] = 6 # change to magenta

    return output_grid
```
