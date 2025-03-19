"""
The transformation involves identifying the leftmost and rightmost green pixels in each row and filling the space between them with green color.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    # Find coordinates of all pixels with the specified color.
    return np.argwhere(grid == color)

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Iterate over each row in the grid.
    for row_index in range(output_grid.shape[0]):
        # Find the coordinates of all green (3) pixels in the current row.
        green_pixels = find_pixels_by_color(output_grid[row_index : row_index+1, :], 3)

        # If there are at least two green pixels in the row.
        if len(green_pixels) >= 2:
            # Get column indices of the green pixels, relative to the row.
            green_cols = green_pixels[:, 1]

            # Find the leftmost and rightmost green pixel column indices.
            start_col = min(green_cols)
            end_col = max(green_cols)

            # Fill the space between the leftmost and rightmost green pixels with green.
            for col in range(start_col + 1, end_col):
                output_grid[row_index, col] = 3

    return output_grid