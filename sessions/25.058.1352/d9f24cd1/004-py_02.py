"""
The transformation applies a vertical red line pattern to the output grid, overwriting every other column (starting with the second column, index 1) with red (2). The pixels in the even-indexed columns (0, 2, 4, ...) from the input grid are preserved in the output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Apply red lines, overwriting odd-indexed columns
    for j in range(output_grid.shape[1]):
        if j % 2 == 1:
            for i in range(output_grid.shape[0]):
                output_grid[i, j] = 2

    return output_grid