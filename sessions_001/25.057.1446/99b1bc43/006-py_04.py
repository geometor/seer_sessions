"""
1. Create Output Grid: Create a 4x4 output grid filled with black (0).
2. Locate Input Block: Identify the 2x2 block at the bottom-right corner of the *input* grid.
3. Copy to Output: Copy the 2x2 block from the input grid to the bottom-right corner of the output grid.
4. Fill Remaining: Set all remaining pixels in the output to 0.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid as all zeros with size 4x4
    output_grid = np.zeros((4, 4), dtype=int)

    # Get the dimensions of the input grid
    input_height, input_width = input_grid.shape

    # Extract the bottom-right 2x2 block from the input grid
    # Handle cases where the input grid is smaller than 2x2
    start_row = max(0, input_height - 2)
    start_col = max(0, input_width - 2)
    block = input_grid[start_row:, start_col:]

    # Copy the block to the bottom-right corner of the output grid
    output_row_start = 4 - block.shape[0]
    output_col_start = 4 - block.shape[1]
    output_grid[output_row_start:, output_col_start:] = block

    return output_grid