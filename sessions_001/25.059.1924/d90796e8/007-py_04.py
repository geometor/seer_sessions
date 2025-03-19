"""
1. Preserve '5': Identify all pixels with the value '5' (gray). These pixels remain unchanged in the output grid.
2. Top Row Transformation: Examine the pixels in the first (top) row of the input grid.
3. Conditional Change: If a pixel in the top row is not equal to '8', it becomes an '8' in the output grid.
4. Preserve Other Rows: All other rows remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Top Row Transformation: Iterate through the top row.
    for j in range(output_grid.shape[1]):
        # Conditional Change: If a pixel is not '8', change it to '8'.
        if output_grid[0, j] != 8:
            output_grid[0, j] = 8

    # Preserve '5' and other rows (already handled by copying the input grid)
    return output_grid