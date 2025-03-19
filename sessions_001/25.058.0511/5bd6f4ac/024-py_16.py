"""
The transformation identifies the bottom-rightmost non-zero pixel in the input grid and places its value in the bottom-right corner of a 3x3 output grid.
"""

import numpy as np

def find_bottom_right_nonzero(grid):
    """
    Finds the bottom-rightmost non-zero pixel in the grid.
    Returns the pixel value and its coordinates, or (None, (None, None)) if no non-zero pixel is found.
    """
    rows, cols = grid.shape
    for i in range(rows - 1, -1, -1):
        for j in range(cols - 1, -1, -1):
            if grid[i, j] != 0:
                return grid[i, j], (i, j)
    return 0, (None, None)

def transform(input_grid):
    # Initialize output_grid as 3x3 with zeros
    output_grid = np.zeros((3, 3), dtype=int)

    # Find the bottom-rightmost non-zero pixel
    pixel_value, _ = find_bottom_right_nonzero(input_grid)

    # Place the pixel value in the bottom-right corner of the output grid
    output_grid[2, 2] = pixel_value

    return output_grid