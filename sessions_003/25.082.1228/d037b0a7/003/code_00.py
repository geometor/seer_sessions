"""
The transformation rule involves propagating colors downwards within each column independently. For each column, the first non-zero value encountered is propagated downwards, replacing all subsequent zeros in that column. If a column contains only zeros, it remains unchanged.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through Columns
    for c in range(cols):
        # Find First Non-Zero in Column
        fill_value = 0  # Default to 0 if no non-zero value is found
        for r in range(rows):
            if output_grid[r, c] != 0:
                fill_value = output_grid[r, c]
                break  # Stop searching after finding the first non-zero

        # Propagate fill_value down the column (only if a non-zero was found)
        if fill_value != 0:
            for r in range(rows):
                if output_grid[r,c] !=0:
                    for r_below in range(r+1, rows):
                        output_grid[r_below,c] = fill_value

    return output_grid