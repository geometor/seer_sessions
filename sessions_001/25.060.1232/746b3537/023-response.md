# 746b3537 • 023 • refine_coder

---
```python
"""
1.  **Identify Row Blocks:** Examine the input grid and identify contiguous "blocks" of rows where all rows within the block have the same color across their entire width.
2.  **Extract Representative Colors:** For each identified row block, extract the color of the first pixel in the first row of that block. This color represents the entire block.
3.  **Construct Output Grid:** Create a new grid with a single column. For each representative color extracted in step 2, add that color to the output grid as a single element of a single column. The output grid has a height equal to the number of row blocks.
"""

import numpy as np

def identify_row_blocks(grid):
    """Identifies contiguous row blocks with the same color."""
    row_blocks = []
    start_row = 0
    for i in range(1, len(grid)):
        if not np.array_equal(grid[i], grid[start_row]):
            row_blocks.append((start_row, i - 1))
            start_row = i
    row_blocks.append((start_row, len(grid) - 1))  # Add the last block
    return row_blocks

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = []

    # 1. Identify Row-Blocks
    row_blocks = identify_row_blocks(input_grid)

    # 2. Extract Representative Colors & 3. Construct Output Grid
    for start, end in row_blocks:
        # Extract the color from the first element of the row-block
        output_grid.append([input_grid[start][0]])

    return output_grid
```
