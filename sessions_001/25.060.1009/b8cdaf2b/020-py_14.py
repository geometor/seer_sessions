"""
The transformation rule is as follows:
1. Identify the third row from the top of the input grid.
2. Change the color of the leftmost and rightmost cells of this third row to blue (1).
3. All other pixels in the input grid remain unchanged and are preserved in the output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows = output_grid.shape[0]

    # Check if there are at least 3 rows before proceeding
    if rows >= 3:
        # Change the color of the leftmost and rightmost pixels of the third row to blue (1)
        output_grid[2, 0] = 1
        output_grid[2, -1] = 1

    return output_grid