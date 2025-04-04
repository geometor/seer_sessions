"""
1.  **Iterate** through each row of the input grid.
2.  For each row:
    *   Start from the leftmost pixel and move to the right.
    *   Replace all the following pixel values on that row with the value of the starting pixel.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid by expanding each pixel's color to the right across its row."""

    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Iterate through each row
    for i in range(rows):
        # Iterate through each pixel in the row from left to right
        for j in range(cols):
            # Expand the current pixel's color to the right
            for k in range(j, cols):
                output_grid[i][k] = input_grid[i][j]

    return output_grid