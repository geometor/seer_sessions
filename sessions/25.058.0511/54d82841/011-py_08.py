"""
The transformation rule is to find the single white (0) pixel in the input grid and change it to yellow (4) in the output grid, keeping all other pixels the same.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid by changing the white pixel to yellow."""
    # Create a copy of the input grid to serve as the output grid.
    output_grid = np.copy(input_grid)

    # Find the coordinates of the white pixel.
    white_pixels = np.where(input_grid == 0)
    white_pixel_row = white_pixels[0][0]
    white_pixel_col = white_pixels[1][0]

    # Change the white pixel to yellow in the output grid.
    output_grid[white_pixel_row, white_pixel_col] = 4

    return output_grid