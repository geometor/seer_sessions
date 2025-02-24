"""
The output grid is 1x1. Its color depends on the number of white pixels
surrounding the gray regions. If the gray pixels are entirely surrounded by
white pixels, the output is black (0). Otherwise, if any gray pixel touches the
edge of the input grid, the output is blue (1).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid
    output_grid = np.zeros((1, 1), dtype=int)

    # Find gray pixels
    gray_pixels = np.argwhere(input_grid == 5)

    # Check if any gray pixel touches the boundary
    touches_boundary = False
    for r, c in gray_pixels:
        if r == 0 or r == input_grid.shape[0] - 1 or c == 0 or c == input_grid.shape[1] - 1:
            touches_boundary = True
            break

    # Set output pixel based on boundary condition
    if touches_boundary:
        output_grid[0, 0] = 1  # Blue
    else:
        output_grid[0, 0] = 0  # Black

    return output_grid