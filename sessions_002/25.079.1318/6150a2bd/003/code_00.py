"""
1. Reverse the order of the rows in the input grid.
2. Identify the cells that were in the *top row* of the *original* input grid.
3. In the cells identified in step 2, swap the following values:
    *   If the value is 3, change it to 8.
    *   If the value is 8, change it to 3.
4. Leave all other cells unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid.
    output_grid = np.copy(input_grid)
    original_top_row_indices = list(range(input_grid.shape[1])) # Capture original top row *column* indices


    # Reverse the order of rows.
    output_grid = np.flipud(output_grid)

    # Apply the value mapping *only* to elements that were originally on the top row.
    for j in original_top_row_indices:
        if input_grid[0, j] == 3:
            output_grid[-1, j] = 8  # -1 index is the *last* row (originally the top)
        elif input_grid[0, j] == 8:
            output_grid[-1, j] = 3

    return output_grid