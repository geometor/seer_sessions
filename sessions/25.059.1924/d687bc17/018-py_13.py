"""
1. Preserve Borders: Keep the top and bottom horizontal bands, and the leftmost and rightmost vertical bands, unchanged.
2. Clear Interior: Set all pixels located *within* the inner region (i.e., not part of the preserved borders) to black (0).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Clear the interior region. Iterate through all rows and columns,
    # excluding the first and last row/column, and set their values to 0.
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            output_grid[r, c] = 0

    return output_grid