# 2bcee788 • 004 • example_1 • investigate_coder

---
```python
"""
The transformation involves filling the background with green and converting a connected shape of yellow and red pixels to an entirely yellow shape, keeping its position in the original grid.
"""

import numpy as np

def find_object(grid, colors):
    # Find the bounding box of the object with specified colors
    rows, cols = grid.shape
    min_row, min_col = rows, cols
    max_row, max_col = -1, -1

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] in colors:
                min_row = min(min_row, r)
                min_col = min(min_col, c)
                max_row = max(max_row, r)
                max_col = max(max_col, c)

    if max_row == -1:  # No object found
        return None

    return (min_row, min_col, max_row, max_col)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.full(input_grid.shape, 3)  # Fill with green (3)

    # Find the object with yellow and red
    object_bbox = find_object(input_grid, [2, 4])

    if object_bbox:
        min_row, min_col, max_row, max_col = object_bbox

        # change output pixels within bounding box
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                if input_grid[r, c] == 4:
                    output_grid[r,c] = 4
                if input_grid[r, c] == 2:
                    output_grid[r, c] = 4  # Change red (2) to yellow (4)

    return output_grid
```
