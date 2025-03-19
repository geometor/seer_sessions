# 3345333e • 012 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find all contiguous regions of the same color in the input grid. These constitute the objects.
2.  **Process Magenta Objects:** For each object, if its color is magenta, find its outline. Replace the magenta object with its outline.
3.  **Preserve Other Objects:** All other non-magenta objects found in the input grid should be kept without modification.
4. **Construct Output:** combine updated magenta outlines and other color objects to create a complete output.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous regions of non-zero pixels and returns them as a list of objects.
       Each object is a dictionary with 'color' and 'pixels' (list of (row, col) tuples).
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def _dfs(row, col, color, pixels):
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] != color:
            return
        visited.add((row, col))
        pixels.append((row, col))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            _dfs(row + dr, col + dc, color, pixels)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] != 0 and (row, col) not in visited:
                color = grid[row, col]
                pixels = []
                _dfs(row, col, color, pixels)
                objects.append({'color': color, 'pixels': pixels})
    return objects

def get_object_outline(pixels, rows, cols):
    """
    Get only the outline pixels of the object, where the object is solid
    """

    pixel_set = set(pixels)
    outline_pixels = []

    for row, col in pixels:
        is_outline = False
        # Check neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            n_row, n_col = row + dr, col + dc
            if not (0 <= n_row < rows and 0 <= n_col < cols) or (n_row, n_col) not in pixel_set:
                is_outline = True
                break  # If any neighbor is not part of the object or outside, it's outline
        if is_outline:
          outline_pixels.append((row, col))
    return outline_pixels

def transform(input_grid):
    # initialize output_grid with the original input
    output_grid = input_grid.copy()
    rows, cols = input_grid.shape

    # Find objects
    objects = find_objects(input_grid)

    # Find magenta outlines and keep, preserve other objects
    for obj in objects:
        if obj['color'] == 6:
            magenta_outline = get_object_outline(obj['pixels'], rows, cols)
            # first clear original magenta object
            for row, col in obj['pixels']:
              output_grid[row, col] = 0
            # then make the outline
            for row, col in magenta_outline:
                output_grid[row, col] = 6

    return output_grid
```
