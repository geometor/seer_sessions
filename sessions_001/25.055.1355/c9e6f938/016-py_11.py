"""
The output grid's dimensions are determined by adding 2 to both the height and width of the input grid.
An orange pixel is placed in the output grid at a position two rows below and two columns to the right of its original position in the input grid.
Another orange pixel is placed at a location two rows down and two columns from the left edge.
"""

import numpy as np

def find_orange_pixel(grid):
    # Find the coordinates of the orange pixel (value 7).
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r,c] == 7:
                return (r, c)
    return None

def transform(input_grid):
    # Initialize output_grid by adding 2 to both height and width.
    output_grid = np.zeros((input_grid.shape[0] + 2, input_grid.shape[1] + 2), dtype=int)

    # Find the orange pixel in the input grid.
    orange_pixel_coords = find_orange_pixel(input_grid)

    if orange_pixel_coords:
      # Place the first orange pixel two rows and columns offset from input.
      output_grid[orange_pixel_coords[0] + 2, orange_pixel_coords[1] + 2] = 7
      # Place the second orange pixel two down and two columns from left edge.
      output_grid[orange_pixel_coords[0] + 2, 2] = 7

    return output_grid