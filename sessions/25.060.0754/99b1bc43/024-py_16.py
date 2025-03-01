"""
The transformation considers the top-left 4x4 region of the input grid. This region is divided into four 2x2 non-overlapping blocks. Each 2x2 block is examined: if all pixels are 0, the output remains 0; if all are 1, the output is 3; if all are 2, the output is 3; if all are 4, the output is 0. If mixed, the output is the value of first element.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a 4x4 array
    output_grid = np.zeros((4, 4), dtype=int)

    # Iterate through 2x2 blocks in the input_grid, taking only the relevant parts
    for i in range(2):
        for j in range(2):
            # Extract the 2x2 subgrid
            subgrid = input_grid[i*2:(i+1)*2, j*2:(j+1)*2]

            # Apply color mapping based on subgrid values
            if np.all(subgrid == 0):
                output_grid[i*2:(i+1)*2, j*2:(j+1)*2] = 0
            elif np.all(subgrid == 1):
                output_grid[i*2:(i+1)*2, j*2:(j+1)*2] = 3
            elif np.all(subgrid == 2):
                output_grid[i*2:(i+1)*2, j*2:(j+1)*2] = 3                
            elif np.all(subgrid == 4):
                output_grid[i*2:(i+1)*2, j*2:(j+1)*2] = 0
            else:
                 output_grid[i*2:(i+1)*2, j*2:(j+1)*2] = subgrid[0,0]

    return output_grid