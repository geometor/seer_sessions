"""
The transformation preserves the horizontal gray lines of '5's and converts all other non-5 digits to 0 (white).
"""

import numpy as np

def find_horizontal_lines(grid, value):
    # Find rows where all elements are equal to the given value.
    line_indices = []
    for i, row in enumerate(grid):
        if all(pixel == value for pixel in row):
            line_indices.append(i)
    return line_indices

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # find the gray lines
    gray_lines = find_horizontal_lines(input_grid, 5)

    # change output pixels
    for r in range(rows):
        for c in range(cols):
             if r not in gray_lines:
                if output_grid[r,c] !=5:
                    output_grid[r,c] = 0
    return output_grid