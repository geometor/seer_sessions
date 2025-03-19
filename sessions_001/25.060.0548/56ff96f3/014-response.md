# 56ff96f3 • 014 • refine_coder

---
```python
"""
Expands colored regions in a grid. Green (3) pixels expand downwards, and also one pixel to the right of each expanded pixel. Orange (7) pixels expand rightwards, until they reach the edge of the grid.
"""

import numpy as np

def get_objects(grid):
    objects = []
    for row_idx, row in enumerate(grid):
        for col_idx, pixel in enumerate(row):
            if pixel != 0:
                objects.append((pixel, row_idx, col_idx))
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    objects = get_objects(input_grid)

    # change output pixels
    for color, row, col in objects:
        if color == 3: # green
            for i in range(row, len(output_grid)):
                output_grid[i,col] = 3
                if col + 1 < len(output_grid[i]):  # Corrected: Check bounds of *current* row
                    output_grid[i,col+1] = 3
        elif color == 7: # orange
            for j in range(col, len(output_grid[row])):
                output_grid[row, j] = 7

    return output_grid
```
