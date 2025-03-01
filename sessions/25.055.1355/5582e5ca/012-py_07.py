"""
The transformation rule identifies the outer "frame" or "border" of the input grid and changes it to maroon (9). If the input grid is a single-color rectangle, the entire grid is considered the border and becomes maroon. If there's an inner area of a different color, only the outermost layer of pixels is transformed to maroon.
"""

import numpy as np

def find_outer_rectangle(grid):
    """Finds the outermost rectangle in a grid."""
    rows, cols = grid.shape
    top_left = (0, 0)
    bottom_right = (rows - 1, cols - 1)
    return top_left, bottom_right, grid[0,0] # return the color of the outer rectangle too

def transform(input_grid):
    """
    Transforms the input grid by changing the outer rectangle to maroon (9).
    """
    # initialize output_grid with the same dimensions and type as the input
    output_grid = np.copy(input_grid)

    # find outer rectangle
    top_left, bottom_right, color = find_outer_rectangle(input_grid)

    # change the found rectangle in the output grid to maroon
    rows, cols = output_grid.shape
    for i in range(rows):
        for j in range(cols):
            if (i == top_left[0] or i == bottom_right[0] or
                j == top_left[1] or j == bottom_right[1]):
                output_grid[i, j] = 9


    return output_grid