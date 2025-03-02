"""
The output grid has the same width as the input grid but half the height.
Maroon (9) pixels in the input grid are transformed to red (2) pixels in the
output grid, with their positions horizontally mirrored within their
respective rows. The vertical position is mapped to the corresponding row in
the reduced-height output grid. Blue (1) pixels in the input are transformed
to red (2) pixels at the same relative horizontal location, mapped to the
reduced output dimensions. White (0) pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid
    input_height, input_width = input_grid.shape
    output_height = input_height // 2
    output_width = input_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Transform Maroon and Blue Pixels, and retain white.
    for i in range(input_height):
        for j in range(input_width):
            output_row = i % output_height
            if input_grid[i, j] == 9:
                output_grid[output_row, input_width - 1 - j] = 2
            elif input_grid[i, j] == 1:
                output_grid[output_row, j] = 2
            elif input_grid[i, j] == 0:
                output_grid[output_row, j] = 0


    return output_grid