"""
The transformation rule involves extending each non-zero colored object in the input grid vertically downwards in the output grid. The output grid has the same width as the input grid, and the output grid's height is fixed at 10, based on the examples. The input grid is copied to the output grid. Then, for each column, if a pixel in the input grid has a non-zero color, all pixels directly below it in the output grid, up to the bottom, are set to that same color. Pixels in the output grid without a non-zero color directly above them in the input remain unchanged (initialized to 0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extending each non-zero pixel downwards to
    the bottom of the output grid. The output grid has dimensions 10 x width of input.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    input_grid = np.array(input_grid)
    rows_in = input_grid.shape[0]
    cols_in = input_grid.shape[1]

    # Determine output dimensions (rows = 10, cols = same as input)
    rows_out = 10
    cols_out = cols_in

    # Initialize output_grid with zeros
    output_grid = np.zeros((rows_out, cols_out), dtype=int)

    # Copy the input grid to the output grid
    output_grid[:rows_in, :] = input_grid

    # Iterate through each column
    for c in range(cols_in):
        # Iterate through each row of the *input* grid
        for r in range(rows_in):
            # If the current cell in the *input* is non-zero
            if input_grid[r, c] != 0:
                # Fill down the output grid
                for r_below in range(r, rows_out):
                    output_grid[r_below, c] = input_grid[r, c]

    return output_grid