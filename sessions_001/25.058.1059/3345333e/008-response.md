# 3345333e • 008 • example_1 • investigate_coder

---
```python
"""
Identifies a magenta (6) outline and a blue (1) object inside it. 
Removes the blue object and keeps the magenta outline.
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
    """
    Removes the blue object within magenta outline from grid
    """
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find objects
    objects = find_objects(input_grid)

    magenta_pixels = []
    blue_pixels = []

    for obj in objects:
        if obj['color'] == 6:
            magenta_pixels.extend(obj['pixels'])
        elif obj['color'] == 1:
            blue_pixels.extend(obj['pixels'])
            
    magenta_outline = get_object_outline(magenta_pixels, rows, cols)

    # change output pixels
    for row, col in magenta_outline:
      output_grid[row, col] = 6


    return output_grid
```
