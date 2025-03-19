"""
The input grid is replicated twice within a larger 9x9 grid. One copy is placed at the top-right corner, and another at the bottom-left corner. The rest of the 9x9 grid is filled with zeros (white).
"""

import numpy as np

def transform(input_grid):
    # Initialize a 9x9 output grid filled with zeros.
    output_grid = np.zeros((9, 9), dtype=int)

    # Get the dimensions of the input grid.
    input_height, input_width = input_grid.shape

    # Place the first copy of the input grid at the top-right corner.
    output_grid[0:input_height, 6:9] = input_grid

    # Place the second copy of the input grid at the bottom-left corner.
    output_grid[6:9, 0:input_width] = input_grid

    return output_grid