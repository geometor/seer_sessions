"""
The transformation involves two steps:
1. Reverse the order of rows in the input grid.
2. Apply a value mapping where 3 becomes 8, 8 becomes 3, and other values remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid (we'll modify it).
    output_grid = np.copy(input_grid)

    # Reverse the order of rows.
    output_grid = np.flipud(output_grid)

    # Apply the value mapping.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] == 3:
                output_grid[i, j] = 8
            elif output_grid[i, j] == 8:
                output_grid[i, j] = 3

    return output_grid