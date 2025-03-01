"""
Ignores the input grid values and creates a new grid with the same dimensions, filled with a repeating checkerboard pattern of 1, 2, and 4, starting with 2 at the top-left corner.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid into a checkerboard pattern.
    """
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Fill the grid with the checkerboard pattern
    for i in range(rows):
        for j in range(cols):
            if (i + j) % 3 == 0:
                output_grid[i, j] = 2
            elif (i + j) % 3 == 1:
                output_grid[i, j] = 4
            else:
                output_grid[i, j] = 1

    return output_grid