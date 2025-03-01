"""
Embed the input grid into a larger output grid, duplicate the first row and last column of the input, and pad the remaining cells with 0.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with zeros, larger than input grid.
    output_grid = np.zeros((input_grid.shape[0] + 1, input_grid.shape[1] + 1), dtype=int)

    # Embed the input grid into the output grid.
    output_grid[1:input_grid.shape[0]+1, 1:input_grid.shape[1]+1] = input_grid

    # Duplicate the first row of the input.
    output_grid[0, 1:input_grid.shape[1]+1] = input_grid[0, :]

    # Duplicate the last column of the input.
    output_grid[1:input_grid.shape[0]+1, input_grid.shape[1]] = input_grid[:, -1]
    
    #Duplicate copied row and col
    output_grid[0, input_grid.shape[1]] = input_grid[0, -1]
    output_grid[input_grid.shape[0], input_grid.shape[1]] = input_grid[-1,-1]

    
    return output_grid