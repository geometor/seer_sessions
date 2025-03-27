"""
1.  **Identify Central White Columns:** Find the starting and ending indices of the contiguous vertical columns of `0`s (white) that divide the input grid.

2.  **Mirror Colors:**
    *   Starting at the left edge of the central white column (index `central_white_column_start`), work outwards to the left edge and note the cell colors.
    *   Mirror the color values into their correct mirrored locations.

3. **Transfer Colors:**
    * transfer leftmost colors
        * starting from the central white columns and working left, replace
          values with leftmost column values
    * transfer rightmost colors
        * transfer the values from the rightmost column to the leftmost columns
"""

import numpy as np

def find_central_zeros(grid):
    """Finds the starting index of the central columns of zeros."""
    num_cols = grid.shape[1]
    for j in range(num_cols):
        if np.all(grid[:, j] == 0):
            return j
    return -1  # Should not happen in these examples

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    num_rows, num_cols = input_grid.shape

    # 1. Find the central "white" (0-valued) columns
    zero_col_start = find_central_zeros(input_grid)

    # 2. Mirror Colors
    left_end = zero_col_start -1
    right_start = zero_col_start

    while left_end >= 0:
        for i in range(num_rows):
            output_grid[i, right_start] = input_grid[i,left_end]

        right_start += 1
        left_end -= 1
        
    # 3. transfer values

    # transfer rightmost
    for j in range(zero_col_start):
      if(j < num_cols):
        for i in range(num_rows):
            output_grid[i,j] = input_grid[i, num_cols - 1]

    # transfer leftmost
    leftmost_col = input_grid[:, 0].copy()  # avoid modifying input
    first_zero_col_idx = -1

    for j in range(num_cols):
        if all(input_grid[:,j] == 0):
            first_zero_col_idx = j
            break

    if first_zero_col_idx != -1:
        next_col_idx = first_zero_col_idx
        for i in range(num_rows):
          output_grid[i,next_col_idx] = leftmost_col[i]

    return output_grid