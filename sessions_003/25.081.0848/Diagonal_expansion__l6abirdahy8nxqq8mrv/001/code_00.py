"""
For each non-white pixel in the input grid, draw a cross of that color in the output grid, centered at the same row and column. Fill the rest of the output grid with white.
"""

import numpy as np

def get_non_white_pixels(grid):
    """
    Finds the coordinates and colors of non-white pixels in the grid.
    """
    non_white_pixels = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                non_white_pixels.append((r, c, grid[r, c]))
    return non_white_pixels

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    output_grid = np.zeros_like(input_grid)
    non_white_pixels = get_non_white_pixels(input_grid)

    for r, c, color in non_white_pixels:
        # Draw horizontal line of the cross
        for i in range(output_grid.shape[1]):
            output_grid[r, i] = color
        # Draw vertical line of the cross
        for i in range(output_grid.shape[0]):
            output_grid[i, c] = color

    return output_grid