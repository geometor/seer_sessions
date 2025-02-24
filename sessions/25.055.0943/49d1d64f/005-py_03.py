"""
The transformation scales a 2x2 input grid to a 6x6 output grid.  The input is
scaled by a factor of 3. A border of width 1 and color black (0) is added
around the scaled input.
"""

import numpy as np

def transform(input_grid):
    # Determine the scaling factor and border width.
    scale_factor = 3
    border_width = 1
    border_color = 0

    input_height, input_width = input_grid.shape

    # Create the output grid with the correct dimensions.
    output_height = input_height * scale_factor + 2 * border_width
    output_width = input_width * scale_factor + 2 * border_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Populate the scaled input within the output grid.
    for i in range(input_height):
        for j in range(input_width):
            for x in range(scale_factor):
                for y in range(scale_factor):
                    output_grid[i * scale_factor + border_width + x, j * scale_factor + border_width + y] = input_grid[i, j]

    return output_grid