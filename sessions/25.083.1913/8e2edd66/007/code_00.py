"""
The transformation rule involves identifying non-zero pixels in the input grid and mapping them to a 9x9 output grid. The mapping involves scaling the input coordinates to the output coordinates, and inverting the row indices.
"""

import numpy as np

def get_non_zero_pixels(input_grid):
    # Find the non-zero color in the input grid
    pixels = []
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r, c] != 0:
                pixels.append((r,c, input_grid[r,c]))
    return pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((9, 9), dtype=int)
    input_height = input_grid.shape[0]
    input_width = input_grid.shape[1]

    # Find Input Pixels
    input_pixels = get_non_zero_pixels(input_grid)

    # change output pixels based on a mapping of input pixels

    for r_in, c_in, color in input_pixels:
        if (input_height > 1) and (input_width > 1):
            r_out = (input_height - 1 - r_in) * (9 - 1) // (input_height - 1)
            c_out = c_in * (9 - 1) // (input_width - 1)
        elif (input_height == 1) and (input_width > 1):
            r_out = (input_height - 1 - r_in) * 8
            c_out = c_in * (9 - 1) // (input_width - 1)
        elif (input_width == 1) and (input_height > 1):
            r_out = (input_height - 1 - r_in) * (9-1) // (input_height - 1)
            c_out = c_in * 8
        else: # input_height == 1 and input_width == 1:
            r_out = (input_height - 1 - r_in) * 8
            c_out = c_in * 8

        output_grid[r_out, c_out] = color
        

    return output_grid