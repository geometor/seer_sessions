"""
1. Identify Non-White Pixels: Find all pixels in the input grid that are not white (color 0).
2. Diagonal Cross Creation: For each non-white pixel:
    *   Create a diagonal cross in the output grid, using the same color as the identified pixel.
    *   The center of this cross is the original location (row and column) of the non-white pixel.
    *   The cross extends diagonally in four directions:
        *   Up-Left:  Extend from the center pixel towards the top-left corner of the grid.
        *   Up-Right: Extend from the center pixel towards the top-right corner of the grid.
        *   Down-Left: Extend from the center pixel towards the bottom-left corner of the grid.
        *   Down-Right: Extend from the center pixel towards the bottom-right corner of the grid.
3. Background: All other pixels in the output grid not part of any diagonal cross will have the default value of 0.
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
    Transforms the input grid according to the diagonal cross rule.
    """
    output_grid = np.zeros_like(input_grid)
    non_white_pixels = get_non_white_pixels(input_grid)

    for r, c, color in non_white_pixels:
        # Draw diagonal lines
        # Up-Left
        i, j = r, c
        while i >= 0 and j >= 0:
            output_grid[i, j] = color
            i -= 1
            j -= 1

        # Up-Right
        i, j = r, c
        while i >= 0 and j < output_grid.shape[1]:
            output_grid[i, j] = color
            i -= 1
            j += 1

        # Down-Left
        i, j = r, c
        while i < output_grid.shape[0] and j >= 0:
            output_grid[i, j] = color
            i += 1
            j -= 1

        # Down-Right
        i, j = r, c
        while i < output_grid.shape[0] and j < output_grid.shape[1]:
            output_grid[i, j] = color
            i += 1
            j += 1

    return output_grid