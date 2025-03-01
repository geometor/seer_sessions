"""
The transformation identifies the location of the first non-zero pixel in the input grid.
Then it determines the output grid size. Output height and width = input height -1.
The output is all-black (0) square grid with corners set to green(3).
"""

import numpy as np

def get_output_size(input_grid):
    # output size is a square: height & width are input_grid height - 1
    h, _ = input_grid.shape
    return h - 1

def transform(input_grid):
    # determine the output grid size
    output_size = get_output_size(input_grid)

    # initialize output_grid with all zeros (black)
    output_grid = np.zeros((output_size, output_size), dtype=int)
    
    # Populate corners of the output_grid with green (3)
    output_grid[0, 0] = 3
    output_grid[0, -1] = 3
    output_grid[-1, 0] = 3
    output_grid[-1, -1] = 3

    return output_grid