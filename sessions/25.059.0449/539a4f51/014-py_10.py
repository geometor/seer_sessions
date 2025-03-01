"""
1. Expand Grid: Double both the height and width of the input grid to create the output grid.
2. Replicate: Copy the *entire* input grid into the top-left quadrant of the output grid.
3. Repeat: Copy the top-left quadrant (which now contains the original input) to the top-right, bottom-left, and bottom-right quadrants of the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 2, input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # copy input to top-left quadrant
    output_grid[:input_height, :input_width] = input_grid

    # repeat top-left to top-right
    output_grid[:input_height, input_width:] = input_grid

    # repeat top-left to bottom-left
    output_grid[input_height:, :input_width] = input_grid

    # repeat top-left to bottom-right
    output_grid[input_height:, input_width:] = input_grid

    return output_grid