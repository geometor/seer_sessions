"""
Connects green pixels horizontally within each row that contains green pixels in the input grid.
"""

import numpy as np

def get_green_pixels_in_row(grid, row_index):
    """
    Returns a list of (row, col) tuples for green pixels in the specified row.
    """
    green_pixels = []
    for col_index, pixel in enumerate(grid[row_index]):
        if pixel == 3:
            green_pixels.append((row_index, col_index))
    return green_pixels

def transform(input_grid):
    """
    Connects green pixels horizontally in a grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    for row_index in range(rows):
        green_pixels = get_green_pixels_in_row(output_grid, row_index)

        # If the row contains green pixels, connect them
        if green_pixels:
            min_col = min(p[1] for p in green_pixels)
            max_col = max(p[1] for p in green_pixels)
            for col_index in range(min_col, max_col + 1):
                output_grid[row_index, col_index] = 3

    return output_grid