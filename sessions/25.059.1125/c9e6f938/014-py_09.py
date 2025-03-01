"""
1.  **Check Input Width:** Determine the width of the input grid.

2.  **Conditional Transformation:**
    *   **If** the input grid's width is exactly 3:
        *   Create an output grid with double the width of the input grid and the same height.
        *   Copy all pixels from the input grid to their corresponding positions in the output grid.
        *   Identify all contiguous horizontal blocks of orange (7) pixels in the input grid.
        *   For each identified orange block, extend it to the right in the output grid by a length equal to the original block's length. The cells to the right are filled.

    *   **Otherwise (if the width is not 3):**
        *   The output grid is identical to the input grid (identity transformation).
"""

import numpy as np

def find_contiguous_blocks(grid, color):
    """Finds contiguous horizontal blocks of a given color."""
    blocks = []
    rows, cols = grid.shape
    for r in range(rows):
        in_block = False
        start_col = 0
        for c in range(cols):
            if grid[r, c] == color:
                if not in_block:
                    in_block = True
                    start_col = c
            elif in_block:
                in_block = False
                blocks.append((r, start_col, c - 1))
        if in_block:
            blocks.append((r, start_col, cols - 1))
    return blocks

def transform(input_grid):
    # Check Input Width
    if input_grid.shape[1] == 3:
        # Create output grid with double width
        output_grid = np.zeros((input_grid.shape[0], input_grid.shape[1] * 2), dtype=int)

        # Copy all pixels from input to output
        for r in range(input_grid.shape[0]):
            for c in range(input_grid.shape[1]):
                output_grid[r, c] = input_grid[r, c]

        # Identify orange blocks
        orange_blocks = find_contiguous_blocks(input_grid, 7)

        # Duplicate orange blocks
        for block in orange_blocks:
            row, start_col, end_col = block
            block_length = end_col - start_col + 1
            for i in range(block_length):
                if start_col + block_length + i < output_grid.shape[1]:
                    output_grid[row, start_col + block_length + i] = 7
    else:
        # Identity transformation
        output_grid = input_grid.copy()

    return output_grid