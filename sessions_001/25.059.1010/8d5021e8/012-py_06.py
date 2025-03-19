"""
The transformation identifies a core block of non-white pixels in the input grid and replicates it across and down in the output grid. The output grid's dimensions and the block's placement involve scaling and overlapping, and remaining cells are filled with white.
"""

import numpy as np

def find_core_block(grid):
    """Finds the largest square block of non-white pixels starting from the top-left."""
    rows, cols = grid.shape
    for size in range(min(rows, cols), 0, -1):
        block = grid[0:size, 0:size]
        if np.all(block != 0):  # Assuming 0 is white
            return block
    return None  # No non-white block found

def transform(input_grid):
    """Transforms the input grid by replicating a core block."""
    core_block = find_core_block(input_grid)
    if core_block is None:
        return input_grid # if not found, just return input

    block_rows, block_cols = core_block.shape
    input_rows, input_cols = input_grid.shape

    # Determine the output size.
    # Based on observations: output height appears to expand ~2.5-3x from input
    # width seems to be somewhat proportional to the block size.
    output_rows = int(input_rows * 2.5) + (block_rows -1)
    output_cols = int(input_cols * 2) + (block_cols * 2)- 2


    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Replicate and place the core block with overlapping.
    for i in range(output_rows // (block_rows) + 3):
        for j in range(output_cols // (block_cols) + 2):
            row_start = i * (block_rows // 2)  # Adjusted for overlap
            col_start = j * (block_cols // 2) # Adjusted for overlap

            row_end = min(row_start + block_rows, output_rows)
            col_end = min(col_start + block_cols, output_cols)

            # Only place if we are within bounds
            if row_start < output_rows and col_start < output_cols:
                output_grid[row_start:row_end, col_start:col_end] = core_block[0:row_end - row_start, 0: col_end-col_start]


    return output_grid