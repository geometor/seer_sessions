"""
The input grid (2x2) is expanded to an output grid (4x4). Each pixel in the input grid corresponds to a 2x2 block of pixels in the output grid.
If a pixel in the input grid is white (0), all corresponding pixels in its 2x2 output block are also white (0).
If a pixel in the input is not white (in this case, yellow '4'), then fill the 2x2 block with a 2x2 checkerboard, using yellow (4) and introducing the azure (8), making sure it is not a solid color.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 2, input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # change output pixels
    for i in range(input_height):
        for j in range(input_width):
            if input_grid[i, j] == 0:
                # White pixel expansion
                output_grid[2*i:2*i+2, 2*j:2*j+2] = 0
            else:
                # Colored pixel expansion (checkerboard pattern)
                output_grid[2*i, 2*j] = input_grid[i, j]
                output_grid[2*i+1, 2*j+1] = input_grid[i, j]
                output_grid[2*i, 2*j+1] = 8
                output_grid[2*i+1, 2*j] = 8

    return output_grid