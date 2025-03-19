"""
For each blue (1) pixel in the input grid, draw an azure (8) cross centered on the blue pixel.
The original blue pixel remains unchanged. Other pixels also remain unchanged. The cross consists
of directly adjacent pixels in the four cardinal directions (up, down, left, right), not diagonally.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by drawing an azure cross around each blue pixel.
    The cross only includes pixels directly adjacent (up, down, left, right).
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find all blue pixels
    blue_pixels = np.argwhere(input_grid == 1)

    # For each blue pixel, draw an azure cross (excluding diagonals)
    for row, col in blue_pixels:
        # Place azure pixels adjacent to the blue pixel (cardinal directions only)
        if row > 0:
            output_grid[row - 1, col] = 8  # Above
        if row < rows - 1:
            output_grid[row + 1, col] = 8  # Below
        if col > 0:
            output_grid[row, col - 1] = 8  # Left
        if col < cols - 1:
            output_grid[row, col + 1] = 8  # Right

    return output_grid