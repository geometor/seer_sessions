"""
Copies the upper-left 3x3 area of the input grid to a new 3x3 output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a 3x3 array filled with zeros (white)
    output_grid = np.zeros((3, 3), dtype=int)

    # Copy the 3x3 subgrid from the input to the output
    for i in range(3):
        for j in range(3):
            # Check if the indices are within the bounds of the input grid
            if i < input_grid.shape[0] and j < input_grid.shape[1]:
                output_grid[i, j] = input_grid[i, j]

    return output_grid