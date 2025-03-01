# 54d82841 • 005 • refine_coder

---
```python
"""
1.  **Preserve Magenta:** All pixels that are magenta (6) in the input grid remain unchanged in the output grid.
2.  **Bottom Row Rule:** Examine the bottom row of the input grid.
3.  **Conditional Change:**
    - Iterate over the *other* rows (not the bottom row). If a pixel in another row is a magenta (6), then in the output grid, transform the pixel in the same column position in the *bottom* row into a yellow (4).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each column
    for col in range(cols):
        # Iterate through rows *excluding* the bottom row
        for row in range(rows - 1):
            # Check for magenta (6) in the current cell
            if input_grid[row, col] == 6:
                # Change the corresponding bottom-row pixel to yellow (4)
                output_grid[rows - 1, col] = 4

    return output_grid
```

