"""
The input grid is a 3x3 grid, and the output grid is a 9x9 grid. The output
grid is constructed by replicating the input grid, with conditional padding
based on whether the input grid contains any non-zero elements. If the input
grid contains only zeros when its non-zero values are replaced by zero, only one copy
of input grid will be in output, otherwise tiling occurs.
"""

import numpy as np

def transform(input_grid):
    # Initialize a 9x9 output grid filled with zeros.
    output_grid = np.zeros((9, 9), dtype=int)
    input_rows, input_cols = input_grid.shape

    # Check if the input grid has only zero if replacing the non-zero with zeros
    input_all_zeros = np.count_nonzero(input_grid) == 0
    test_grid = np.copy(input_grid)
    test_grid[test_grid != 0] = 0
    input_could_be_all_zeros = np.array_equal(test_grid, np.zeros_like(input_grid))

    # Place a copy of the input grid at the top-left
    output_grid[:input_rows, :input_cols] = input_grid

    if not input_could_be_all_zeros:
        # Tile horizontally
        for c_offset in range(input_cols, 9, input_cols):
            output_grid[:input_rows, c_offset:c_offset + input_cols] = input_grid

        # Tile vertically
        for r_offset in range(input_rows, 9, input_rows):
              output_grid[r_offset:r_offset + input_rows, :input_cols] = input_grid


    return output_grid