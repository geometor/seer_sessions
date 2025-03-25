"""
1.  **Copy Rows:** Copy the first two rows of the input grid directly to the output grid, maintaining their original positions.

2.  **Generate Third Row:**
    *   Iterate through each cell of the *first* row of the input grid (index `i`).
    *   Check if `i + 2` is within the bounds of the row.
    *   If `i + 2 ` is within bounds, Compare `input_grid[0][i]` with `input_grid[0][i+2]`.
        * If the two values are *not* equal: place the value of `input_grid[0][i]` to `output_grid[2][i]`.
        * if the two values are equal: Place a `6` in `output_grid[2][i]`.
    *   If `i + 2` goes beyond the length of the row, copy `input_grid[0][i]` to `output_grid[2][i]`.

3.  **Output:** The output grid consists of the copied first two rows and the newly generated third row.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = input_grid.copy()
    rows, cols = input_grid.shape
    output_grid = output_grid[:2] #truncate to first two rows

    # Create third row
    if rows >= 2: #ensure we do not exceed input row bounds
        new_row = []
        for i in range(cols):
            if i + 2 < cols:
                if input_grid[0, i] != input_grid[0, i + 2]:
                    # within bound and not matching:  insert input_grid[0,i] at index i
                    new_row.append(input_grid[0,i])
                else:
                    #within bounds and matching, insert 6
                    new_row.append(6)
            else:
                # out of bounds: insert input_grid[0,i] at index i
                new_row.append(input_grid[0,i])

        output_grid = np.vstack([output_grid, new_row])

    return output_grid.tolist()