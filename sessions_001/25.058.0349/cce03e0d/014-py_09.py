"""
The input grid (3x3) is expanded into a 9x9 output grid. The input grid is replicated in a 3x3 pattern within the output grid. The remaining cells of the output grid are filled with 0s.
"""

import numpy as np

def transform(input_grid):
    # Initialize a 9x9 output grid filled with 0s.
    output_grid = np.zeros((9, 9), dtype=int)

    # Get the dimensions of the input grid.
    input_height, input_width = input_grid.shape

    # Iterate through the input grid and place it at the corresponding positions in the output grid.
    for i in range(input_height):
        for j in range(input_width):
            for row_mult in range(3):
                for col_mult in range(3):
                    output_grid[i + row_mult * input_height, j + col_mult * input_width] = input_grid[i, j]
    return output_grid