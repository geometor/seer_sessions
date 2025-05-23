"""
Subsamples the input grid, copying gray (5) pixels from the input to the output at corresponding odd row and odd column positions.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid.  Since we're taking every other row/col,
    # the output dimensions are half the input, rounded up.
    input_rows, input_cols = input_grid.shape
    output_rows = (input_rows + 1) // 2
    output_cols = (input_cols + 1) // 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through odd rows and columns of the input grid.
    for i in range(0, input_rows, 2):
        for j in range(0, input_cols, 2):
            # Map input indices to output indices (integer division by 2).
            output_i = i // 2
            output_j = j // 2

            # Copy the pixel value if it's gray (5).
            if input_grid[i, j] == 5:
                output_grid[output_i, output_j] = 5

    return output_grid