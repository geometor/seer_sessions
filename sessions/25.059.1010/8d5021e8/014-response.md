# 8d5021e8 • 014 • refine_coder

---
```python
"""
1.  Identify the largest contiguous block of non-white pixels in the input grid. This is the "primary object".
2.  If the primary object forms a solid filled rectangle:
    *   Calculate the output grid size:
        *    height = (input.height * 2.5) + primary_object.height - 1
        *    width = (input.width * 2) + (primary_object.width * 2) - 2
    *   Replicate the primary object, overlapping by half its height and width, across and down the output grid, filling it completely, until the output grid dimensions are met or exceeded. Ensure replication begins in the top-left corner of output.
3.  If no such non-white object is found, or if the non-white object is not a solid filled rectangle:
    * The output is identical to the input. Do not change the size or contents of the input grid.
"""

import numpy as np

def find_largest_non_white_block(grid):
    """Finds the largest contiguous block of non-white pixels."""
    rows, cols = grid.shape
    max_size = 0
    best_block = None

    for row_start in range(rows):
        for col_start in range(cols):
            if grid[row_start, col_start] != 0:  # Non-white
                for size in range(1, min(rows - row_start, cols - col_start) + 1):
                    block = grid[row_start:row_start + size, col_start:col_start + size]
                    if np.all(block != 0) and block.size > max_size :
                        if (block.shape[0] * block.shape[1] == size*size) and (len(np.unique(block)) == 1) :
                            max_size = block.size
                            best_block = block
    return best_block

def is_solid_rectangle(block):
    """Checks if a block is a solid rectangle (all pixels are the same non-zero color)."""

    if block is None or block.size == 0:
        return False

    first_color = block.flatten()[0]

    if first_color == 0:
      return False

    return np.all(block == first_color)

def transform(input_grid):
    """Transforms the input grid according to the rules."""
    primary_object = find_largest_non_white_block(input_grid)

    if primary_object is not None and is_solid_rectangle(primary_object):
        # Replicate and expand
        block_rows, block_cols = primary_object.shape
        input_rows, input_cols = input_grid.shape

        output_rows = int(input_rows * 2.5) + block_rows -1
        output_cols = int(input_cols * 2) + (block_cols * 2) - 2

        output_grid = np.zeros((output_rows, output_cols), dtype=int)

        for i in range(output_rows // (block_rows // 2) + 2 ):
            for j in range(output_cols // (block_cols // 2) + 2):
                row_start = i * (block_rows // 2)
                col_start = j * (block_cols // 2)

                row_end = min(row_start + block_rows, output_rows)
                col_end = min(col_start + block_cols, output_cols)
                if row_start < output_rows and col_start < output_cols:
                  output_grid[row_start:row_end, col_start:col_end] = primary_object[0:row_end-row_start, 0:col_end-col_start]

        return output_grid

    else:
        # No change
        return input_grid
```
