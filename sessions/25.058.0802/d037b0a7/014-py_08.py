"""
Copies the first and second rows of the input grid and pastes them into the third row of the output grid, effectively replacing the original third row.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Copy the first row to the third row.
    output_grid[2, :] = input_grid[0, :]
    
    #Copy the second row to the third row
    output_grid[2, :] = input_grid[1, :]


    return output_grid