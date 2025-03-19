"""
The transformation rule is to double the dimensions of the input grid while maintaining the initial checkerboard pattern. The 2x2 input becomes a building block that repeats to form the 4x4 output.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with dimensions twice the size of the input grid.
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 2, input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Replicate the 2x2 input grid to fill the 4x4 output grid.
    for i in range(output_height):
        for j in range(output_width):
            output_grid[i, j] = input_grid[i % input_height, j % input_width]

    return output_grid