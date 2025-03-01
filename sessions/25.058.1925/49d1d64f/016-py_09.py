"""
Expands a 3x3 input grid to a 5x5 output grid by replicating the input grid values and padding with zeros.
"""

import numpy as np

def transform(input_grid):
    # Initialize a 5x5 output grid with zeros.
    output_grid = np.zeros((5, 5), dtype=int)

    # Copy the input grid to the center of the output grid.
    for i in range(3):
        for j in range(3):
            output_grid[i + 1][j + 1] = input_grid[i][j]

    return output_grid