"""
The transformation removes the rightmost column (all blue pixels) and the bottom row (all blue pixels) from the input grid. Then it exchanges last row and last column.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by removing the rightmost column and bottom row.
    Then exchanges last row and last column.
    """
    # Create a copy of the input grid to avoid modifying the original.
    output_grid = np.copy(input_grid)

    # Get the dimensions of the input grid.
    height, width = output_grid.shape

    # Remove last row
    output_grid = output_grid[:-1,:]
    # Remove the rightmost column.
    output_grid = output_grid[:, :-1]

    # Add a new row and a new column
    height, width = output_grid.shape
    output_grid = np.pad(output_grid, ((0,1),(0,1)), 'constant', constant_values=0)


    # Get new dimensions
    height, width = output_grid.shape

    # Exchange last row with last column after removing the rightmost column.
    last_row = output_grid[height-2,:]
    last_col = output_grid[:,width-2]

    output_grid[:,width-1] = last_row
    output_grid[height-1,:] = last_col


    return output_grid