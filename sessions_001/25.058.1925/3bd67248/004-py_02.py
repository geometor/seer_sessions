"""
The transformation rule is as follows:
1. Keep the magenta (6) pixels from the input grid.
2. Create a diagonal line of red (2) pixels, starting from the top-right corner and moving down-left until it meets the magenta line on the left.
3. Fill the last row of the output grid with yellow (4) pixels.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Create the diagonal red line.
    for i in range(rows):
        # output_grid[row_index, col_index]
        output_grid[i, cols - 1 - i] = 2

    # Fill the last row with yellow.
    output_grid[-1, :] = 4

    return output_grid