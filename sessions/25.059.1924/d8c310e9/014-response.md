# d8c310e9 • 014 • refine_coder

---
```python
"""
1.  **Identify 2x1 Vertical Red Blocks:** Locate all 2x1 vertical blocks of red (color 2) pixels in the input grid, but *only* if they start in the third or fourth row (zero-indexed rows 2 and 3).
2.  **Copy Red Blocks:** Copy the identified vertical red blocks to the same location in the output grid.
3.  **No Extensions**: Do not extend any red blocks.
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

    # Find vertical red blocks
    red_blocks = find_vertical_red_blocks(input_grid, rows, cols)
    
    # only copy red blocks if in 2nd or 3rd row (zero indexed)
    red_blocks_filtered = [(r,c) for r, c in red_blocks if r in [2,3]]

    # Copy red blocks
    for r, c in red_blocks_filtered:
        output_grid[r][c] = 2
        output_grid[r+1][c] = 2
        
    return output_grid
```
