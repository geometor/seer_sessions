"""
Locate the colored pixel in the input. Change its color to red (2) and move it to the top-left corner of the grid. Ensure all other pixels are white (0).
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

    # If colored pixel not exists, return all zero array
    if colored_pixel_location is None:
        return output_grid

    # Change the color of the pixel to red (2) and place at top-left
    output_grid[0, 0] = 2

    return output_grid