"""
The input grid is duplicated. One copy is placed at the bottom of a new grid. the other copy is flipped upside down and placed at the top of the new output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    rows_in = len(input_grid)
    cols_in = len(input_grid[0])
    rows_out = 2* rows_in
    cols_out = cols_in

    output_grid = np.zeros((rows_out, cols_out), dtype=int)
    
    # flip the input_grid and place it at the top of output grid
    flipped_grid = np.flipud(input_grid)

    output_grid[:rows_in, :] = flipped_grid

    # copy the input_grid and place it at the bottom of the output grid.
    output_grid[rows_in:,:] = input_grid

    return output_grid