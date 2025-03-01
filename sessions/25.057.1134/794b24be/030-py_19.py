"""
Find the colored pixel in the input grid. Move this pixel to the top-left corner of the grid (0, 0), preserving its original color. Set all other pixels in the output grid to white (0). If the input grid contains no colored pixels, return a copy of the input.
"""

import numpy as np

def find_colored_pixel(grid):
    # Find the indices of the non-zero elements
    indices = np.nonzero(grid)
    # Return the coordinates as a tuple
    if len(indices[0]) > 0:
        return (indices[0][0], indices[1][0])
    else:
        return None # Return None if no non-zero pixel

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find the colored (non-zero) pixel in the input grid
    colored_pixel_location = find_colored_pixel(input_grid)

    # If colored pixel exists, move it to top-left and keep original color
    if colored_pixel_location:
        row, col = colored_pixel_location
        output_grid[0, 0] = input_grid[row, col]
        return output_grid
    else: #handle all zero input
        return input_grid.copy()