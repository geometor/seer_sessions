# d8c310e9 • 012 • refine_coder

---
```python
"""
1.  **Copy Last Row:** Copy the last row of the input grid to the last row of the output grid.
2.  **Identify Red Blocks:** Find all 2x1 vertical red blocks (color 2) in the third and fourth rows of the input grid.
3. **Copy and Extend, every other:** Copy any vertical red blocks identified in step two. Extend (copy) the red block two cells to its right.
"""

import numpy as np

def find_vertical_red_blocks(grid, rows, cols):
    red_blocks = []
    for r in range(rows - 1):
        for c in range(cols):
            if grid[r][c] == 2 and grid[r+1][c] == 2:
                red_blocks.append((r, c))
    return red_blocks

def transform(input_grid):
    # initialize output_grid as a copy of input
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Copy the last row (already done during initialization)

    # Find vertical red blocks
    red_blocks = find_vertical_red_blocks(input_grid, rows, cols)
    
    red_blocks_filtered = [(r,c) for r, c in red_blocks if r in [2,3]] # only copy red blocks if in 2nd or 3rd row (zero indexed)

    # Copy and extend red blocks
    for i, (r, c) in enumerate(red_blocks_filtered):
        # Copy existing red blocks (already in place due to copy)

        # Extend red blocks to the right by two
        if (i % 2 == 0): # every other
            if c + 2 < cols:
                output_grid[r, c + 2] = 2
                output_grid[r + 1, c + 2] = 2

    return output_grid
```
