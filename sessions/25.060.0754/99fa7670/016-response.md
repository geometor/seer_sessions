# 99fa7670 • 016 • example_3 • investigate_coder

---
```python
"""
1. **Identify Objects:** Find all non-zero pixels in the input grid. Each of these represents a distinct object.
2. **Horizontal Expansion**. For each object, starting from its original location, expand the object's color horizontally to the right edge of the grid.
3.  **Vertical Expansion:** Each expanded object will expand down one row
"""

import numpy as np

def find_objects(grid):
    """Finds all non-zero pixels and returns them as a list of (row, col, color) tuples."""
    objects = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                objects.append((r, c, grid[r, c]))
    return objects

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    output_grid = np.copy(input_grid)
    objects = find_objects(input_grid)

    for r, c, color in objects:
        # Horizontal Expansion
        for c2 in range(c, output_grid.shape[1]):
            output_grid[r, c2] = color
        # Vertical Expansion - one row down.
        if r + 1 < output_grid.shape[0]:
             for c2 in range(c, output_grid.shape[1]):
                output_grid[r+1, c2] = color
    return output_grid
```
