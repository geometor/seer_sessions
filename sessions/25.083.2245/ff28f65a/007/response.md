```python
"""
1.  **Input:** A 2D grid (`input_grid`) of arbitrary size, with cell values representing colors.

2.  **Output:** A 3x3 grid (`output_grid`), initialized with all zeros.

3.  **Find 2x2 Red Blocks:** Scan the `input_grid` and identify all 2x2 blocks where *all* four cells are red (value 2). Record the top-left corner coordinates (row, column) of each such block.

4.  **Divide Input Grid into Nine Regions:**  Conceptually divide the `input_grid` into nine equal regions, corresponding to the cells of the `output_grid`. The size of the regions are *ceilings* of the input grid dimensions divided by three.

5.  **Populate Output Grid:** For each cell (out_row, out_col) in the `output_grid` (ranging from 0 to 2):
    *   Calculate the boundaries of the corresponding region in the `input_grid`:
        *   `row_start = out_row * ceil(rows / 3)`
        *   `row_end = (out_row + 1) * ceil(rows / 3)`
        *   `col_start = out_col * ceil(cols / 3)`
        *   `col_end = (out_col + 1) * ceil(cols / 3)`
    *   Iterate through the list of 2x2 red blocks found in Step 3.
    *   For each red block, check if its top-left corner coordinates (block_row, block_col) fall *within* the current region's boundaries:
        *   `row_start <= block_row < row_end`
        *   `col_start <= block_col < col_end`
    *   If the red block's top-left corner is within the region, set the corresponding `output_grid[out_row, out_col]` to 1. Stop checking further blocks for this region (only one '1' is needed per region).
    * If no red block found, output stays as zero.

6. **Return** The 3x3 `output_grid`.
"""

import numpy as np
from math import ceil

def find_2x2_blocks(grid, color):
    """Finds all 2x2 blocks of the specified color in the grid."""
    blocks = []
    rows, cols = grid.shape
    for i in range(rows - 1):
        for j in range(cols - 1):
            if (grid[i:i+2, j:j+2] == color).all():
                blocks.append((i, j))  # Store top-left corner coordinates
    return blocks

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((3, 3), dtype=int)

    # Calculate region boundaries using ceil
    row_div = ceil(rows / 3)
    col_div = ceil(cols / 3)
    

    # Scan for Red Blocks
    red_blocks = find_2x2_blocks(input_grid, 2)

    # Determine output based on regions
    for out_row in range(3):
        for out_col in range(3):
            row_start = out_row * row_div
            row_end = (out_row + 1) * row_div
            col_start = out_col * col_div
            col_end = (out_col + 1) * col_div

            for block_row, block_col in red_blocks:
                if row_start <= block_row < row_end and col_start <= block_col < col_end:
                    output_grid[out_row, out_col] = 1
                    break  # Once a block is found in the region, set to 1 and move to next

    return output_grid.tolist()
```