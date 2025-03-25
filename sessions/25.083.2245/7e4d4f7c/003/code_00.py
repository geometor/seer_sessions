"""
1.  **Copy Rows:** Copy the first two rows of the input grid directly to the output grid, maintaining their original positions.
2.  **Generate Third Row:**
    *   Iterate through each cell of the *first* row of the input grid (index `i`).
    *   Compare the value of the current cell (`input_grid[0][i]`) with the value two cells to its right (`input_grid[0][i+2]`).
    *    If `i + 2` is within bounds of the row *and* the values are equal: insert `6` into the third row of the *output* grid at the corresponding column index.
    *    If the values at `input_grid[0][i]` and `input_grid[0][i + 2]` are *not* equal, or if `i + 2 ` is beyond the row length, then copy the value in `input_grid[0][i]` to `output_grid[2][i]`.
3.  **Output:** The output grid consists of the copied first two rows and the newly generated third row.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = input_grid.copy()
    rows, cols = input_grid.shape
    output_grid = output_grid[:2] #truncate

    # Create third row
    if rows >= 2: #ensure we do not exceed input row bounds
        new_row = []
        for i in range(cols):
            if i + 2 < cols and input_grid[0, i] == input_grid[0, i + 2]:
                # within bound and matching
                new_row.append(6)
            else:
                # out of bounds, or not matching
                new_row.append(input_grid[0,i])

        output_grid = np.vstack([output_grid, new_row])

    return output_grid.tolist()