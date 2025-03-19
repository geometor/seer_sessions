# 760b3cac • 016 • refine_coder

---
```python
"""
Reflects pixels across the horizontal center line within the top three rows of the input grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid as a copy of the input
    grid = np.array(input_grid)
    output_grid = np.copy(grid)
    rows, cols = grid.shape

    # Determine the horizontal center of the grid
    center_col = cols // 2

    # Iterate through the top three rows
    for r in range(min(3, rows)):
        # Iterate through columns up to the center
        for c in range(center_col):
            # Reflect pixels across the center line, considering odd/even width
            if cols % 2 == 0: # even number of columns
                output_grid[r, cols - 1 - c] = grid[r, c]
            else: # odd number of columns
                output_grid[r, cols - 1 - c] = grid[r, c]

        if (cols % 2 != 0):
            # for odd number of columns keep the center column
            output_grid[r,center_col] = grid[r,center_col]

    return output_grid.tolist()
```
