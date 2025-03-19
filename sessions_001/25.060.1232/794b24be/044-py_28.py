"""
Transform the input grid to the output grid based on the following rule:
All pixels in the top row of the input grid are changed to red (2) in the output grid.
All pixels not in the top row remain white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    # Initialize the output grid as a copy of the input grid, but with all zeros.
    output_grid = np.zeros_like(input_grid)

    # Get the dimensions of the grid
    rows, cols = input_grid.shape

    # Iterate through the top row (row 0)
    for j in range(cols):
        # Change all pixels in the top row to red (2)
        output_grid[0, j] = 2

    return output_grid