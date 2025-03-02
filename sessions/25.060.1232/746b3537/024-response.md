# 746b3537 • 024 • refine_coder

---
```python
"""
1. **Identify Row-Blocks:** Divide the input grid into "row-blocks." A row-block is a group of one or more consecutive rows that contain the *same set of colors*. The order of the colors within each row of the block does *not* matter.

2.  **Extract Unique Colors:** For each row-block, identify the *unique* color values present within that block.

3.  **Construct Output Grid:** Create a new, one-column grid. For *each* row-block:
    *   Determine the *number of rows* in the row-block (its height).
    *   For each unique color identified in step 2, append that color to the output grid a number of times equal to the row-block's height. Maintain the order of colors as they appear in the original.
"""

import numpy as np

def identify_row_blocks(grid):
    """Identifies contiguous row blocks with the same set of colors."""
    row_blocks = []
    start_row = 0
    current_colors = set(grid[0])
    for i in range(1, len(grid)):
        if set(grid[i]) != current_colors:
            row_blocks.append((start_row, i - 1, tuple(sorted(current_colors))))
            start_row = i
            current_colors = set(grid[i])
    row_blocks.append((start_row, len(grid) - 1, tuple(sorted(current_colors))))  # Add the last block
    return row_blocks

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""
    input_grid = np.array(input_grid)

    # 1. Identify Row-Blocks
    row_blocks = identify_row_blocks(input_grid)

    # 2. Extract Unique Colors (already done within identify_row_blocks)

    # 3. Construct Output Grid
    output_grid = []
    for start, end, colors in row_blocks:
        block_height = end - start + 1
        for color in colors:
            for _ in range(block_height):
                output_grid.append([color])

    return output_grid
```
