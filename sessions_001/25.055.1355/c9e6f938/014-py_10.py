"""
Duplicate the orange pixel and place one at the original x,y and one copy on the far right side of output, same row.
"""

import numpy as np

def find_orange_pixel(grid):
    # Find the coordinates of the orange pixel (value 7).
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r,c] == 7:
                return (r, c)
    return None  # Should not happen in this specific task, but good practice.


def transform(input_grid):
    # Initialize output_grid with double the width of the input_grid.
    output_grid = np.zeros((input_grid.shape[0], input_grid.shape[1] * 2), dtype=int)

    # Find the orange pixel in the input grid.
    orange_pixel_coords = find_orange_pixel(input_grid)

    if orange_pixel_coords:
      # Place the original orange pixel.
      output_grid[orange_pixel_coords[0], orange_pixel_coords[1]] = 7
      # Place the duplicated orange pixel on the right edge.
      output_grid[orange_pixel_coords[0], output_grid.shape[1] - 1] = 7

    return output_grid