"""
Identifies blue (1) pixels in the input grid and creates green (3) pixels 
vertically centered on each blue pixel's location.
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

    # Iterate through each blue pixel
    for row, col in blue_pixels:
        # Place green pixel in the same row and column
        output_grid[row, col] = 3

        # Place green pixel one row above
        if row - 1 >= 0:
            output_grid[row - 1, col] = 3

        # Place green pixel one row below
        if row + 1 < input_grid.shape[0]:
            output_grid[row + 1, col] = 3

    return output_grid.tolist()