"""
The input grid is replicated as a 2x2 matrix within the 3x3 output grid, with the spaces surrounding the 2x2 matrix of grids filled with zero.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((9, 9), dtype=int)

    # Get input grid dimensions
    input_height, input_width = input_grid.shape

    # Replicate and place the input grid in a 2x2 pattern
    for i in range(2):
        for j in range(2):
            # Calculate the starting row and column for each replica
            start_row = i * (input_height + 3)
            start_col = j * (input_width + 3)

            # Place the replica into the output grid
            output_grid[start_row:start_row + input_height, start_col:start_col + input_width] = input_grid

    return output_grid