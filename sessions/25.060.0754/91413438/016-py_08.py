"""
1. Tile: Replicate the input grid nine times in a 3x3 pattern to create a larger grid.
2. Locate Blue: find the row index of the blue pixel in the original input grid.
3. Zero Rows: Based on the row index from step 2 (input_blue_row), zero out the
   three rows starting at index `input_blue_row * 3` to `input_blue_row*3+2`
   inclusive.
"""

import numpy as np

def find_blue_row(grid):
    # Find the row index of the blue pixel (value 1).
    rows, cols = np.where(np.array(grid) == 1)
    if len(rows) > 0:
        return rows[0]  # Return the first blue pixel's row.
    return 0 # default in case no blue pixel is found.

def transform(input_grid):
    # Tile the input grid 3x3.
    tiled_grid = np.tile(np.array(input_grid), (3, 3))

    # Find the row index of the blue pixel in the input grid.
    blue_row = find_blue_row(input_grid)

    # Calculate the starting row index to zero out.
    start_row = blue_row * 3

    # Zero out the three rows.
    tiled_grid[start_row:start_row+3, :] = 0

    return tiled_grid.tolist()