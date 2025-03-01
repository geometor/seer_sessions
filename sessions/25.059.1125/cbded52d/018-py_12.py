"""
The transformation involves identifying two green pixels in the same row and filling the space between them with green color.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    # Find coordinates of all pixels with the specified color.
    return np.argwhere(grid == color)

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find the coordinates of all green (3) pixels.
    green_pixels = find_pixels_by_color(input_grid, 3)

    # Check if there are exactly two green pixels.
    if len(green_pixels) == 2:
        # Extract row and columns for the green pixels.
        row1, col1 = green_pixels[0]
        row2, col2 = green_pixels[1]

        # Ensure they are on the same row.
        if row1 == row2:
            # Determine the start and end columns.
            start_col = min(col1, col2)
            end_col = max(col1, col2)

            # Fill the space between the two green pixels with green.
            for col in range(start_col + 1, end_col):
                output_grid[row1, col] = 3

    return output_grid