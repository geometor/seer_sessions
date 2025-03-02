# 746b3537 • 020 • example_5 • investigate_coder

---
```python
"""
1. **Identify Row-Blocks:** Divide the input grid into "row-blocks". A row-block is a group of one or more consecutive rows where *all* the cells in each row have the *same* color value.

2. **Extract Representative Colors:** For each identified row-block, extract the single color value that represents all cells within that block.

3. **Construct Output Grid:** Create a new 1-dimensional grid (a single column).  Each element in this output grid corresponds to a row-block in the input grid, in their original vertical order (from top to bottom). The value of each element in output grid will be representative color of its corresponding row block.

4. The result will be a 1-dimensional grid listing a sequence of color values, where the sequence corresponds to the color of each row block in the input from top to bottom.
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
    """Transforms the input grid according to the defined rule."""
    input_grid = np.array(input_grid)
    
    # 1. Identify Row-Blocks
    row_blocks = identify_row_blocks(input_grid)

    # 2. Extract Representative Colors & 3. Construct Output Grid
    output_grid = []
    for start, end in row_blocks:
        # Extract the color from the first element of the row-block (since all are the same)
        output_grid.append([input_grid[start][0]])

    return output_grid
```
