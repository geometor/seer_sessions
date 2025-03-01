"""
Expands each pixel of the input grid into a 2x2 block in the output grid,
maintaining the original color. Adds a one-pixel wide white (0) border around
the entire output grid and between the 2x2 blocks.
"""

import numpy as np

def transform(input_grid):
    # Calculate output grid dimensions: (2*height + 1, 2*width + 1)
    output_height = 2 * input_grid.shape[0] + 1
    output_width = 2 * input_grid.shape[1] + 1

    # Initialize output_grid with zeros (white)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through input grid and expand pixels
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            # Place the 2x2 block in output_grid, starting at (2i+1, 2j+1)
            output_grid[2*i + 1, 2*j + 1] = input_grid[i, j]
            output_grid[2*i + 1, 2*j + 2] = input_grid[i, j]
            output_grid[2*i + 2, 2*j + 1] = input_grid[i, j]
            output_grid[2*i + 2, 2*j + 2] = input_grid[i, j]

    return output_grid