"""
The input is a grid of pixels, each with a color value (0-9). For every pixel in the input grid, create a 2x2 block of pixels in the output grid. The 2x2 block will have the same color value as the corresponding input pixel.  The output is a grid with twice the height and twice the width of the input.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height = 2 * input_height
    output_width = 2 * input_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # change output pixels 
    for i in range(input_height):
        for j in range(input_width):
            output_grid[2*i:2*i+2, 2*j:2*j+2] = input_grid[i, j]

    return output_grid