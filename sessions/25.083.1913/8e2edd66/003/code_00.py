"""
The input grid's non-zero pixels are expanded and mirrored into a 9x9 grid. The precise mapping is complex but involves mirroring across both horizontal and vertical axes.
"""

import numpy as np

def get_non_zero_color(input_grid):
    # Find the non-zero color in the input grid
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i, j] != 0:
                return input_grid[i, j]
    return 0

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((9, 9), dtype=int)
    input_height = input_grid.shape[0]
    input_width = input_grid.shape[1]

    # Find the non-zero color
    color = get_non_zero_color(input_grid)
    if color == 0:
      return output_grid

    # Find Input Pixels
    input_pixels = []
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r,c] == color:
                input_pixels.append((r,c))

    # change output pixels based on a mirroring of input pixels

    for r_in, c_in in input_pixels:
        r_out = r_in * (8 // (input_height -1))
        c_out = c_in * (8 // (input_width - 1))
        output_grid[r_out, c_out] = color

        # mirror horizontally
        output_grid[r_out, 8-c_out] = color

        #mirror vertically
        output_grid[8-r_out, c_out] = color
        
        # mirror both
        output_grid[8-r_out, 8-c_out] = color
        

    return output_grid