"""
The transformation rule is a two-step expansion. First, each pixel in the input 3x3 grid is expanded horizontally to become two pixels.  Then, each resulting row is duplicated to create a 6x6 grid.

"""

import numpy as np

def transform(input_grid):
    # Initialize an empty 3x6 grid for the first expansion phase.
    intermediate_grid = np.zeros((3, 6), dtype=int)

    # Horizontal expansion: Each pixel becomes two.
    for i in range(3):
        for j in range(3):
            intermediate_grid[i, 2*j] = input_grid[i, j]
            intermediate_grid[i, 2*j + 1] = input_grid[i, j]

    # Initialize the final 6x6 output grid.
    output_grid = np.zeros((6, 6), dtype=int)

    # Vertical expansion: Duplicate each row from the intermediate grid.
    for i in range(3):
        output_grid[2*i, :] = intermediate_grid[i, :]
        output_grid[2*i + 1, :] = intermediate_grid[i, :]
        
    return output_grid