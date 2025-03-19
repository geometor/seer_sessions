# 93b581b8 • 012 • refine_coder

---
```python
"""
1.  **Identify the 2x2 Block:** Locate the contiguous 2x2 block of non-zero pixels within the input grid.

2.  **Preserve 2x2 Block:** Copy the 2x2 block from the input grid to the *exact same position* in the output grid.

3.  **Top Reflection:**
    *   Place the value of the top-right pixel of the 2x2 block into the top-left cell (0, 0) of the output grid.
    *   Place two copies of the bottom-left pixel of the 2x2 block at the *end* of the first row of the output grid.

4.  **Bottom Replication:**
    *   Mirror the top row of the 2x2 block (e.g., [a, b] becomes [b, a]).
    *   Starting *two rows below* the bottom edge of the 2x2 block, place the mirrored row.
    *   Repeat the mirrored row *again* in the row immediately below.

5.  **Padding:** Fill all other cells in the output grid with 0 (black).
"""

import numpy as np

def find_2x2_block(grid):
    """Finds the top-left coordinates of the 2x2 block of non-zero pixels."""
    rows, cols = grid.shape
    for i in range(rows - 1):
        for j in range(cols - 1):
            if (grid[i, j] != 0 and grid[i+1, j] != 0 and
                grid[i, j+1] != 0 and grid[i+1, j+1] != 0):
                return (i, j)
    return None

def transform(input_grid):
    """Transforms the input grid according to the rules."""
    output_grid = np.zeros_like(input_grid)
    block_start = find_2x2_block(input_grid)

    if block_start:
        i, j = block_start
        # Preserve 2x2 block
        output_grid[i:i+2, j:j+2] = input_grid[i:i+2, j:j+2]

        # Top Reflection
        top_right = input_grid[i, j+1]
        bottom_left = input_grid[i+1, j]
        output_grid[0, 0] = top_right
        output_grid[0, -1] = bottom_left
        output_grid[0, -2] = bottom_left

        # Bottom Replication
        mirrored_row = input_grid[i, j:j+2][::-1]
        output_grid[i+3, j:j+2] = mirrored_row
        output_grid[i+4, j:j+2] = mirrored_row

    return output_grid
```
