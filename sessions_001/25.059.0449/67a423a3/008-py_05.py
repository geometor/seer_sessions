"""
White pixels become Yellow unless a Green pixel exists above or below, *or*
unless a yellow pixel exists to the left.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # iterate through each cell of the input_grid
    for r in range(rows):
        for c in range(cols):
            # preservation of non-white pixel
            if input_grid[r, c] != 0:
                continue

            # conditional change for white pixels
            is_above_green = (r > 0 and input_grid[r-1, c] == 3)
            is_below_green = (r < rows - 1 and input_grid[r+1, c] == 3)
            is_left_yellow = (c > 0 and input_grid[r, c-1] == 4)

            if not (is_above_green or is_below_green or is_left_yellow):
                 output_grid[r, c] = 4

    return output_grid