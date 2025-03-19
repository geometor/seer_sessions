"""
1.  **Preserve Zeroes:** All zero-valued (white) pixels in the input grid remain zero-valued in the output grid.
2.  **Left Column to Right Column:** Any non-zero pixel in the leftmost column (index 0) of the input grid is copied to the rightmost column (index -1) of the output grid.  The non-zero pixel's row position on the right is calculated from the input as one less than the input row.
3.  **Clear other non-zero cells:** set the value of all the other non-zero pixels to 0
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Preserve Zeroes and Clear other non-zero cells
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] == 0:
                output_grid[i, j] = 0  # Keep 0s in place
            else:
                output_grid[i,j] = 0

    # Left Column to Right Column
    for i in range(rows):
        if input_grid[i, 0] != 0:
            output_grid[i - 1, cols - 1] = input_grid[i, 0]

    return output_grid