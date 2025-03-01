"""
1.  **Copy the Top Row:** The bottom row of the output grid starts as an exact copy of the top row of the input grid.
2.  **Conditional Color Change:** For each pixel in the bottom row, check the color of the pixel directly above it in the middle row.
3.  **Apply Rule:**
    *   If the pixel in the middle row is black (0), change the corresponding pixel in the bottom row to yellow (4).
    *   Otherwise, keep the pixel in the bottom row the same color as its corresponding pixel in the top row.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # get the number of columns
    num_cols = output_grid.shape[1]

    # iterate over each column index
    for col_index in range(num_cols):
        # check if the pixel directly above the bottom row (in the middle, assumed to be 2nd, or index 1 row) is black (0)
        if input_grid[1, col_index] == 0:
            # if it's black, change the corresponding pixel in the bottom row to yellow (4)
            output_grid[2, col_index] = 4
        else:
            # Otherwise, keep the pixel in the bottom row the same color as its corresponding pixel in the top row.
            output_grid[2, col_index] = input_grid[0, col_index]

    return output_grid