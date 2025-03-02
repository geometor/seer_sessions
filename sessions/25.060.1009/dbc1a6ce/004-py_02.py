"""
For each blue (1) pixel in the input grid, draw an azure (8) cross centered on the blue pixel.
The original blue pixel remains unchanged. Other pixels also remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by drawing an azure cross around each blue pixel.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find all blue pixels
    blue_pixels = np.argwhere(input_grid == 1)

    # For each blue pixel, draw an azure cross
    for row, col in blue_pixels:
        # Place azure pixels adjacent to the blue pixel
        if row > 0:
            output_grid[row - 1, col] = 8  # Above
        if row < rows - 1:
            output_grid[row + 1, col] = 8  # Below
        if col > 0:
            output_grid[row, col - 1] = 8  # Left
        if col < cols - 1:
            output_grid[row, col + 1] = 8  # Right
        if row > 0 and col > 0: # Top Left
             output_grid[row - 1, col-1] = 8
        if row > 0 and col < cols -1: # Top Right
             output_grid[row - 1, col+1] = 8
        if row < rows -1  and col > 0: # Bottom Left
             output_grid[row + 1, col-1] = 8
        if row < rows -1 and col < cols -1: # Bottom Left
             output_grid[row + 1, col-1] = 8

    return output_grid