"""
Replicates the input grid to create an output grid with dimensions five times the input grid, padding with 0 as needed.
"""

import numpy as np

def transform(input_grid):
    # Determine the dimensions of the input grid.
    input_height, input_width = input_grid.shape

    # Calculate the dimensions of the output grid.
    output_height = input_height * 5
    output_width = input_width * 5

    # Create an output grid filled with 0s.
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Replicate the input grid into the output grid.
    for i in range(5):
        for j in range(5):
            output_grid[i * input_height:(i + 1) * input_height, j * input_width:(j + 1) * input_width] = input_grid

    return output_grid