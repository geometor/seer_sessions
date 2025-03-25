"""
Identifies blue (1) pixels in the input grid. For each column containing blue
pixels, creates a vertical line of three green (3) pixels centered on row 4.
"""

import numpy as np

def find_blue_pixels(grid):
    """Finds the coordinates of all blue (1) pixels in the grid."""
    blue_pixels = []
    for r_idx, row in enumerate(grid):
        for c_idx, pixel in enumerate(row):
            if pixel == 1:
                blue_pixels.append((r_idx, c_idx))
    return blue_pixels

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    blue_pixels = find_blue_pixels(input_grid)

    # if no blue pixels return the original grid
    if not blue_pixels:
        return output_grid.tolist()

    # Group blue pixels by column
    columns_with_blue = {}
    for r, c in blue_pixels:
        if c not in columns_with_blue:
            columns_with_blue[c] = []
        columns_with_blue[c].append(r)

    # Iterate through each column with blue pixels
    for col, rows in columns_with_blue.items():
        # Determine the center row for the green line (always row 4)
        center_row = 4

        # Place green pixel in the center
        output_grid[center_row, col] = 3

        # Place green pixel one row above
        if center_row - 1 >= 0:
            output_grid[center_row - 1, col] = 3

        # Place green pixel one row below
        if center_row + 1 < input_grid.shape[0]:
            output_grid[center_row + 1, col] = 3

    return output_grid.tolist()