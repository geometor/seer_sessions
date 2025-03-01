# 941d9a10 • 014 • refine_coder

---
```python
"""
1.  **Blue Replacement:** The first three white pixels in the first column (starting at the top) are always replaced with blue.
2.  **Red Replacement:** Examine the first column. Starting at the top, find the first run of contiguous white pixels that are *below* the blue pixels. All these pixels in this block are changed to red.
3.  **Green Replacement:** The "last" white pixel in the grid (when traversing in reverse row-major order - bottom-right to top-left) is changed to green, *only if* it is white in the output (after applying the blue and red rules).
4. The program operates by modifying the input grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Blue Replacement: First three white pixels in the first column
    blue_count = 0
    for r_idx in range(rows):
        if output_grid[r_idx, 0] == 0 and blue_count < 3:
            output_grid[r_idx, 0] = 1
            blue_count += 1

    # Red Replacement: Contiguous white pixels below blue in the first column
    red_start = False
    for r_idx in range(rows):
        if output_grid[r_idx, 0] == 1:  # Check for blue pixels
            red_start = True # We passed the blue section
            continue

        if red_start and output_grid[r_idx, 0] == 0:
            output_grid[r_idx, 0] = 2

    # Green Replacement: Last white pixel in reverse row-major order
    for r_idx in reversed(range(rows)):
        for c_idx in reversed(range(cols)):
            if output_grid[r_idx, c_idx] == 0:
                output_grid[r_idx, c_idx] = 3
                return output_grid  # Return immediately after finding the last white pixel

    return output_grid
```
