# 93b581b8 • 014 • refine_coder

---
```python
"""
1.  **Identify the largest square block:** Find the largest square block of non-zero pixels within the input grid that is identical in both the input and output grids at the same location.

2.  **Preserve the Block:** Copy the identified block from the input grid to the *exact same position* in the output grid.

3.  **Top Reflection:**
    *   Place the value of the top-right pixel of the identified block into the top-left cell (0, 0) of the output grid.
    *   Place two copies of the bottom-left pixel of the identified block at the *end* of the first row of the output grid.

4.  **Bottom Replication:**
     *   Let (r,c) be the row and column of the bottom left corner of the identified block.
     *   Place the mirrored row from the top of the identified block, starting two rows below the identified block.
     *   Place the mirrored row from the top of the identified block, starting three rows below the identified block.

5.  **Padding:** Fill all other cells in the output grid with 0 (black).
"""

import numpy as np

def find_largest_square_block(input_grid, output_grid):
    """Finds the largest square block common to both grids."""
    rows, cols = input_grid.shape
    max_block_size = 0
    block_start = None

    for i in range(rows):
        for j in range(cols):
            for k in range(1, min(rows - i, cols - j) + 1):
                sub_input = input_grid[i:i+k, j:j+k]
                if np.array_equal(sub_input, output_grid[i:i+k, j:j+k]):
                    if k > max_block_size:
                        max_block_size = k
                        block_start = (i, j)
    return block_start, max_block_size

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    
    # Find and preserve the block
    block_start, block_size = find_largest_square_block(input_grid, output_grid) #Need output for comparison
    if block_start:
        i, j = block_start
        output_grid[i:i+block_size, j:j+block_size] = input_grid[i:i+block_size, j:j+block_size]

        # Top Reflection
        top_right = input_grid[i, j + block_size - 1]
        bottom_left = input_grid[i + block_size - 1, j]
        output_grid[0, 0] = top_right
        output_grid[0, -1] = bottom_left
        output_grid[0, -2] = bottom_left


        # Bottom Replication
        mirrored_row = input_grid[i, j:j+block_size][::-1]

        # Check if there's enough space before placing the mirrored rows
        if i + block_size + 2 < output_grid.shape[0]:
            output_grid[i + block_size + 1 : i + block_size + 1 + min(2, output_grid.shape[0] - (i+block_size+1)),j:j+block_size] = [mirrored_row, mirrored_row]


    return output_grid
```
