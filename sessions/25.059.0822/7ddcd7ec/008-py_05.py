"""
Identify all green (3) pixels in the input grid. For each green pixel, extend a diagonal line of green pixels downwards and to the right. Continue the extension until the edge of the grid is reached (either the bottom edge, the right edge, or both). All other pixels should become white (0).
"""

import numpy as np

def get_green_pixels(grid):
    # find the coordinates of all green pixels
    green_pixels = []
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value == 3:
                green_pixels.append((r, c))
    return green_pixels

def transform(input_grid):
    # initialize output_grid as all white
    output_grid = np.zeros_like(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # get green pixels
    green_pixels = get_green_pixels(input_grid)

    # change output pixels - extend green pixels diagonally
    for r, c in green_pixels:
        # extend the pixel diagonally
        row, col = r, c
        while row < rows and col < cols:
            output_grid[row][col] = 3
            row += 1
            col += 1

    return output_grid