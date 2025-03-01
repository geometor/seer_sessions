"""
Finds the top-most row in the input grid that contains at least one blue pixel, and replaces all pixels in that row of the output grid with red.
The rest of the output grid pixels are set to white.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid, but all white.
    output_grid = np.zeros_like(input_grid)

    # Find the top-most row with at least one blue pixel.
    top_blue_row = -1
    for i, row in enumerate(input_grid):
        if 1 in row:
            top_blue_row = i
            break  # Stop after finding the first row with a blue pixel

    # If a blue row was found, replace all elements in that row of the output grid with red (2).
    if top_blue_row != -1:
        output_grid[top_blue_row, :] = 2

    return output_grid