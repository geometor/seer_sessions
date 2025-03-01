"""
The transformation rule is to move the row containing all blue pixels (value 1) down by one position. The other rows, containing all white pixels (value 0) shift to fill vacated position. In other words, it's a cyclic permutation on rows, where all rows are moved downwards and last row wraps to the first.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the row with all blue pixels (1s)
    blue_row_index = -1
    for i in range(rows):
        if np.all(input_grid[i] == 1):
            blue_row_index = i
            break

    # Shift the rows down by one (cyclic permutation)
    if blue_row_index != -1:
      new_blue_row_index = (blue_row_index + 1) % rows
      output_grid = np.roll(input_grid, shift=1, axis=0) #roll rows down by 1

    return output_grid