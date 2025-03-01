"""
1.  **Identify the Center:** Locate the cell with the value '0' in the input grid. This is the center point of the transformation.
2.  **Preserve Center**: Copy the value of the *center* pixel of the input grid to the corresponding *center* position on the output grid.
3.  **Invert Colors (Cross Pattern):**
    *   All the values on the input grid are inverted.
    *   A value on the input grid is replaced with 0 on the output grid if and only if:
        *   It is at the top or bottom row, and an odd column number.
        *   It is on the left or right most column, and an odd row number.

In other words, imagine an "X" shape of 0's, and the input number in the center.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # initialize output_grid as a copy of input
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # find center
    center_row, center_col = -1, -1 # avoid UnboundLocalError

    for r in range(rows) :
      for c in range(cols):
        if input_grid[r][c] == 0:
          center_row, center_col = r, c
          break

    # if we can't find the 0, then return same size grid
    if center_row < 0:
        return output_grid


    # Preserve the center pixel
    #output_grid[center_row, center_col] = input_grid[center_row, center_col]

    # Apply the cross pattern replacement, inverting other numbers with 0
    for r in range(rows):
        for c in range(cols):
            if (r == center_row and c == center_col):
                continue

            if (r == 0 or r == rows -1) and (c%2 == 0):
                output_grid[r, c] = 0
            elif  (c == 0 or c == cols -1) and (r%2 == 0) :
                output_grid[r,c] = 0
            elif (r == center_row) or (c == center_col):
                output_grid[r,c] = 0

    return output_grid