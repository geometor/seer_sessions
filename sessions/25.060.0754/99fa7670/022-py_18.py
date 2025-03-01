"""
1.  **Identify** all non-zero pixels in the input grid.
2.  For each non-zero pixel:
    *   Locate the pixel's row.
    *    Starting with the pixel's original column, replace pixel values to right and on the same row, with the non-zero pixel's color, until reaching the right edge of the grid.
3. All other pixels (with original value 0) remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Iterate through each cell in the input grid
    for i in range(rows):
        for j in range(cols):
            # Check if the pixel is non-zero
            if input_grid[i][j] != 0:
                # Expand the color to the right
                for k in range(j, cols):
                    output_grid[i][k] = input_grid[i][j]

    return output_grid