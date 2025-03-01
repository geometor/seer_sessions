"""
Identify the single non-zero pixel (which is blue) in the input grid. Change the color of this pixel to red. Move this pixel to the top-left corner of the grid, coordinates (0, 0). All other pixels in the grid, which are initially white, remain unchanged.
"""

import numpy as np

def find_non_zero_pixel(grid):
    """Finds the coordinates of the non-zero pixel in a grid."""
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] != 0:
                return (i, j)
    return None

def transform(input_grid):
    # Initialize output grid with all zeros and same dimensions as input
    output_grid = np.zeros_like(input_grid)

    # Find the non-zero pixel in the input grid
    non_zero_pixel_coords = find_non_zero_pixel(input_grid)

    # If a non-zero pixel exists, place a red pixel at the top-left corner
    if non_zero_pixel_coords:
        output_grid[0, 0] = 2

    return output_grid