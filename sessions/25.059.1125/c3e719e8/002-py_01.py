"""
The 3x3 input grid is replicated four times.
One copy is in each quadrant of the 9x9 grid
All remaining cells in the 9x9 output grid are filled with '0'.
"""

import numpy as np

def transform(input_grid):
    # Initialize the 9x9 output grid with zeros.
    output_grid = np.zeros((9, 9), dtype=int)

    # Get the dimensions of the input grid.
    input_height, input_width = input_grid.shape

    # Place copies of input in four quadrants
    output_grid[0:3, 0:3] = input_grid
    output_grid[0:3, 6:9] = input_grid
    output_grid[6:9, 0:3] = input_grid
    output_grid[6:9, 6:9] = input_grid
    
    return output_grid