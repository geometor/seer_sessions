"""
The transformation involves iterating through the input grid. '0' (white) pixels are 
replaced with '5' (gray). Non-zero pixels may remain the same or change to '5'.
The logic determining which non-zero pixels to change and which to keep is not fully determined.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Iterate through each cell of the input grid
    rows, cols = output_grid.shape
    for i in range(rows):
        for j in range(cols):
            # If the value is 0, replace it with 5
            if output_grid[i, j] == 0:
                output_grid[i, j] = 5
            # else: # values not zero may or may not be changed to 5
            #   output_grid[i,j] = output_grid[i,j] # keep the original
            #   output_grid[i,j] = 5 # change all to 5

    return output_grid