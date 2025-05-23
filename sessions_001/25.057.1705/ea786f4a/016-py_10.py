"""
The transformation identifies a single white pixel (0) in the input grid and expands it into a cross shape in the output grid. The expansion extends vertically and horizontally from the white pixel's location, stopping when it encounters any color other than white. If no white pixel is found, the output grid is identical to the input grid.
"""

import numpy as np

def find_white_pixel(grid):
    # Find the coordinates of the white pixel (value 0).
    rows, cols = np.where(grid == 0)
    if len(rows) > 0:  # Check if a white pixel was found
        return rows[0], cols[0]
    return None  # Or handle the case where no white pixel is present

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the center white pixel.
    center = find_white_pixel(input_grid)
    if center is None:
        return output_grid # if no center, do nothing
    center_row, center_col = center

    # Expand vertically upwards.
    for r in range(center_row -1, -1, -1):
        if output_grid[r, center_col] != 0:
            break
        output_grid[r, center_col] = 0

    # Expand vertically downwards.
    for r in range(center_row + 1, rows):
        if output_grid[r, center_col] != 0:
            break
        output_grid[r, center_col] = 0

    # Expand horizontally to the left.
    for c in range(center_col - 1, -1, -1):
        if output_grid[center_row, c] != 0:
            break
        output_grid[center_row, c] = 0

    # Expand horizontally to the right.
    for c in range(center_col + 1, cols):
        if output_grid[center_row, c] != 0:
            break
        output_grid[center_row, c] = 0

    return output_grid