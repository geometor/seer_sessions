"""
Find the single non-zero pixel in the input grid, change its color to red, and move it to the center of an output grid of the same size.
"""

import numpy as np

def find_non_zero_pixel(grid):
    # Iterate through the grid to find the non-zero pixel
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] != 0:
                return (i, j)
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of the input, filled with zeros.
    output_grid = np.zeros_like(input_grid)

    # Find the non-zero pixel in the input grid.
    non_zero_pixel_coords = find_non_zero_pixel(input_grid)

    # If a non-zero pixel is found, move it to the center and change its value to 2.
    if non_zero_pixel_coords:
        center_row = output_grid.shape[0] // 2
        center_col = output_grid.shape[1] // 2
        output_grid[center_row, center_col] = 2

    return output_grid