"""
The transformation rule extracts all non-white rows from the input grid,
reverses their order, and places them at the bottom of the output grid,
overwriting the original bottom rows.
"""

import numpy as np

def get_non_white_rows(grid):
    # helper function to get non-white rows
    non_white_rows = []
    for row in grid:
        if np.all(row == row[0]) and row[0] != 0:
            non_white_rows.append(row)
    return non_white_rows

def transform(input_grid):
    # initialize output_grid as a copy of input grid
    output_grid = np.copy(input_grid)
    
    # get non-white rows
    non_white_rows = get_non_white_rows(input_grid)
    
    # reverse the order of non-white rows
    non_white_rows_reversed = non_white_rows[::-1]

    # count how many were extracted    
    num_non_white_rows = len(non_white_rows_reversed)
    
    # overwrite the last n rows of the output with reversed non-white rows
    if num_non_white_rows > 0:
      output_grid[-num_non_white_rows:] = non_white_rows_reversed
    
    return output_grid