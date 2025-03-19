# 2281f1f4 • 006 • refine_coder

---
```python
"""
The transformation rule is as follows:
1. Identify the positions of all gray (5) pixels in the input grid.
2. Identify rows that contain at least one gray pixel.
3. Identify columns that contain at least one gray pixel.
4. Within these identified rows OR columns, change the color of white (0) pixels to red (2).
5. All other white pixels remain unchanged (or are outside the influence of gray pixels).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows_with_gray = set()
    cols_with_gray = set()

    # Find rows and cols with gray pixels
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r, c] == 5:
                rows_with_gray.add(r)
                cols_with_gray.add(c)

    # change white pixels to red if in the target row OR column
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r,c] == 0:
                if r in rows_with_gray or c in cols_with_gray: # Changed AND to OR
                  output_grid[r,c] = 2

    return output_grid
```
