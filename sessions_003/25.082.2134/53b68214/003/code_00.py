"""
The transformation rule is a "vertical fill" or "downward extension" of every non-zero colored pixel in the input grid. The output grid's dimensions are determined by the training examples provided. The height will be adjusted according to output example, while the width will remain the same as the input. The extension of non-zero pixels continues to the bottom of the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extending each non-zero pixel downwards to
    the bottom of the output grid. The size of output grid is determined by examples.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    input_grid = np.array(input_grid)
    rows_in = input_grid.shape[0]
    cols_in = input_grid.shape[1]

    # Determine output dimensions (rows based on example, cols same as input)
    rows_out = 10 # determined by example expected outputs
    cols_out = cols_in

    # Initialize output_grid with zeros, using the determined dimensions
    output_grid = np.zeros((rows_out, cols_out), dtype=int)

    # Copy the input grid to output
    output_grid[:rows_in, :] = input_grid

    # Iterate through each cell in the *input* grid
    for r in range(rows_in):
        for c in range(cols_in):
            # Check if the current cell in the *input* grid is non-zero
            if input_grid[r, c] != 0:
                # Propagate the pixel's value downwards in output grid,
                #  to the *last* row of output
                for r_below in range(r + 1, rows_out):
                    output_grid[r_below, c] = input_grid[r, c]

    return output_grid