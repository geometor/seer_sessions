"""
The input grid (3x3) is transformed into a larger output grid (6x6).  The transformation replicates each non-zero pixel in the input grid diagonally down and to the right in the output grid. The output grid is double the dimensions of the input grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 2, input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # change output pixels
    for row in range(input_height):
        for col in range(input_width):
            pixel_value = input_grid[row, col]
            if pixel_value != 0:
                output_grid[row * 2, col * 2] = pixel_value
                output_grid[row * 2 + 1, col * 2 + 1] = pixel_value

    return output_grid