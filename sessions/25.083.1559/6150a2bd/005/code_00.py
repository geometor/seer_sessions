"""
Rotate the input grid 90 degrees counter-clockwise and remap the values.
"""

import numpy as np

def transform(input_grid):
    # Rotate the input grid 90 degrees counter-clockwise.
    rotated_grid = np.rot90(input_grid, k=-1)
    
    output_grid = np.copy(rotated_grid)

    # Remap values based on observations.
    for i in range(rotated_grid.shape[0]):
        for j in range(rotated_grid.shape[1]):
            if rotated_grid[i, j] == 0:
                output_grid[i, j] = 0
            elif rotated_grid[i, j] == 1:
                output_grid[i, j] = 0
            elif rotated_grid[i, j] == 2:
                output_grid[i, j] = 5
            elif rotated_grid[i, j] == 3:
                output_grid[i,j] = 8 #corrected
            elif rotated_grid[i, j] == 5:
                output_grid[i, j] = 2 #corrected
            elif rotated_grid[i, j] == 7:
                output_grid[i, j] = 7
            elif rotated_grid[i, j] == 8:
                output_grid[i, j] = 3

    return output_grid