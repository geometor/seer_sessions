"""
The transformation involves swapping pairs of pixels around the center pixel of a 3x3 grid.
Specifically:
1. Top-left pixel swaps with top-right.
2. Bottom-left pixel swaps with bottom-right.
3. Top-middle pixel swaps with left-middle.
4. Bottom-middle pixel swaps with right-middle.
The center pixel remains unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Swap top-left and top-right pixels.
    output_grid[0, 0], output_grid[0, 2] = output_grid[0, 2], output_grid[0, 0]

    # Swap bottom-left and bottom-right pixels.
    output_grid[2, 0], output_grid[2, 2] = output_grid[2, 2], output_grid[2, 0]

    # Swap top-middle and left-middle pixels.
    output_grid[0, 1], output_grid[1, 0] = output_grid[1, 0], output_grid[0, 1]

    # Swap bottom-middle and right-middle pixels.
    output_grid[2, 1], output_grid[1, 2] = output_grid[1, 2], output_grid[2, 1]

    return output_grid