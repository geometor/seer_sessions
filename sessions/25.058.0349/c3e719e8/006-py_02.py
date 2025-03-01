"""
The input grid is replicated four times and positioned at four corners in a 9x9 output grid, with 3x3 blocks of '0' inserted between and around the 3x3 pattern to expand the output.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as 9x9 filled with 0s
    output_grid = np.zeros((9, 9), dtype=int)

    # Get input grid dimensions
    input_height, input_width = input_grid.shape

    # Place the input grid in the top-left corner
    output_grid[:input_height, :input_width] = input_grid

    # Place the input grid in the top-right corner
    output_grid[:input_height, 6:9] = input_grid

    # Place the input grid in the bottom-left corner
    output_grid[6:9, :input_width] = input_grid
    
    # place the input grid in the bottom-right corner
    output_grid[6:9,6:9] = input_grid
    

    return output_grid