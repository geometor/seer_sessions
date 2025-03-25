"""
Transforms a grid by zeroing the first three rows, setting the fourth row based on non-zero values in the input's third row,
and setting the fifth row based on 1s in the input's third row.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    
    # Get the number of rows and columns
    rows, cols = input_grid.shape
    
    # Zero out the first three rows
    output_grid[:3, :] = 0

    # create row four
    for j in range(cols):
      if input_grid[2,j] != 0:
        output_grid[3,j] = 5
      else:
        output_grid[3,j] = 0

    # Transform Row 5 based on values in row 3 of input
    for j in range(cols):
        if input_grid[2, j] == 1:
            output_grid[rows - 1, j] = 1
        else:
            output_grid[rows-1, j] = 5

    return output_grid