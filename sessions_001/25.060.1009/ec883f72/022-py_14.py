"""
1.  **Copy Input:** The output grid initially starts the same size as the input grid, but all black.
2.  **Add Red Pixels:** Two red (2) pixels are added at the top row (row 0) of the output grid.
3.  **Column Placement:**
    *   The first red pixel is placed in the first column (column 0).
    *   The second red pixel is placed in the last column (column width - 1).
4.  **Preserve Input:** The input is copied to the output, overwriting any existing,
    so if red was placed where input pixels exist, the input pixels are written
    over top of them.

"""

import numpy as np

def transform(input_grid):
    # Initialize output grid as all black, same dimensions as input
    output_grid = np.zeros_like(input_grid)

    # Add two red pixels at the top row
    output_grid[0, 0] = 2
    output_grid[0, -1] = 2

    #Copy the input grid on top
    output_grid = np.where(input_grid != 0, input_grid, output_grid)

    return output_grid