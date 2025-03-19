"""
Changes zeros to ones if and only if the zero is part of a 2x2 block where the other three pixels are ones.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through all possible 2x2 subgrids
    for i in range(rows - 1):
        for j in range(cols - 1):
            # Check if the current cell is 0 and the other three cells in the 2x2 block are 1
            if input_grid[i, j] == 0:
                if input_grid[i + 1, j] == 1 and input_grid[i, j + 1] == 1 and input_grid[i + 1, j + 1] == 1:
                    output_grid[i,j] = 1
            elif input_grid[i+1,j] == 0:
                if input_grid[i,j] == 1 and input_grid[i,j+1] == 1 and input_grid[i+1,j+1] == 1:
                    output_grid[i+1,j] = 1
            elif input_grid[i,j+1] == 0:
                if input_grid[i,j] == 1 and input_grid[i+1,j] == 1 and input_grid[i+1,j+1] == 1:
                    output_grid[i,j+1] = 1
            elif input_grid[i+1,j+1] == 0:
                if input_grid[i,j] == 1 and input_grid[i+1,j] == 1 and input_grid[i, j+1] == 1:
                    output_grid[i+1,j+1] = 1


    return output_grid.tolist()