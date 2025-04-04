"""
The transformation rule involves identifying orange (7) and blue (1) pixels within the grid.
Orange pixels expand towards blue pixels, filling adjacent empty (0) cells with orange.
Other colored pixels (red/2, green/3) remain unchanged except for displacement.
"""

import numpy as np

def find_pixels(grid, color):
    """Finds the coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color)

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""

    output_grid = np.copy(input_grid)
    orange_pixels = find_pixels(input_grid, 7)
    blue_pixels = find_pixels(input_grid, 1)

    for orange_pixel in orange_pixels:
        for blue_pixel in blue_pixels:
            # Calculate row and column differences
            row_diff = blue_pixel[0] - orange_pixel[0]
            col_diff = blue_pixel[1] - orange_pixel[1]

            # Determine direction of expansion
            row_step = 0
            col_step = 0

            if row_diff > 0:
                row_step = 1
            elif row_diff < 0:
                row_step = -1

            if col_diff > 0:
                col_step = 1
            elif col_diff < 0:
                col_step = -1

            # Expand orange towards blue
            current_row = orange_pixel[0] + row_step
            current_col = orange_pixel[1] + col_step
            # while we are not at the blue and still in bounds, check what is in that cell
            while (current_row != blue_pixel[0] or current_col != blue_pixel[1]) and \
                  (0 <= current_row < input_grid.shape[0]) and (0 <= current_col < input_grid.shape[1]):

                output_grid[current_row, current_col] = 7

                current_row += row_step
                current_col += col_step

    return output_grid