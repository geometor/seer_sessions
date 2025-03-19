"""
The transformation rule is as follows:
1. Change the color of all pixels in the top row of the input grid to gray (5).
2. Change the color of all pixels in the remaining rows (rows 1 and 2) to white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = np.copy(input_grid)  # Create a copy to avoid modifying the original
    rows, cols = output_grid.shape

    # Change the top row to gray (5)
    for j in range(cols):
        output_grid[0, j] = 5

    # Change the remaining rows to white (0)
    for i in range(1, rows):
        for j in range(cols):
            output_grid[i, j] = 0

    return output_grid