"""
1. Identify Starting Pixels: Locate all non-zero pixels in the input grid. These are the starting points for expansion.
2. Expansion: For each non-zero pixel:
    a. Expand the pixel's color horizontally to the right edge of the grid.
    b. Expand downwards. The expansion continues until it hits the bottom of the grid.
3. No Interaction: If two expanding regions would collide, there is no special behavior - the expansion from step 2b simply proceeds.
"""

import numpy as np

def get_non_zero_pixels(grid):
    """Finds the positions of non-zero pixels in the grid."""
    return np.argwhere(grid != 0)

def expand_pixel(grid, start_row, start_col, color):
    """Expands a pixel to a rectangle to the right and down."""
    # Expand right
    for col in range(start_col, grid.shape[1]):
        grid[start_row, col] = color

    # Expand down
    for row in range(start_row + 1, grid.shape[0]):
        for col in range(start_col, grid.shape[1]):
            grid[row, col] = color


def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.zeros_like(input_grid)
    non_zero_pixels = get_non_zero_pixels(input_grid)

    for row, col in non_zero_pixels:
        color = input_grid[row, col]
        expand_pixel(output_grid, row, col, color)

    return output_grid