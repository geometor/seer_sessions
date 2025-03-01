"""
Locate the center pixel of the input grid. If the center pixel is white (0), change it to yellow (4). Leave all other pixels unchanged.
"""

import numpy as np

def get_center_pixel(grid):
    # Get the dimensions of the grid
    rows, cols = grid.shape
    # Calculate the center coordinates
    center_row = rows // 2
    center_col = cols // 2
    return (center_row, center_col)

def transform(input_grid):
    # Create a copy of the input grid to serve as the output grid
    output_grid = np.copy(input_grid)

    # Get center pixel coordinates
    center_row, center_col = get_center_pixel(input_grid)

    # Change the center pixel to yellow (4) if it's white (0)
    if output_grid[center_row, center_col] == 0:
        output_grid[center_row, center_col] = 4

    return output_grid