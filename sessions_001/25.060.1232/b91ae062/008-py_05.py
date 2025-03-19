"""
The input grid is scaled up by a factor of 2 in both the horizontal and vertical directions. Every individual pixel in the input grid is replaced by a 2x2 block of pixels in the output grid. The color of the 2x2 block is identical to the color of the original pixel it replaces.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with doubled dimensions.
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 2, input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel in the input grid.
    for row in range(input_height):
        for col in range(input_width):
            # Replicate the pixel's color to form a 2x2 block in the output grid.
            output_grid[row*2:row*2+2, col*2:col*2+2] = input_grid[row, col]

    return output_grid