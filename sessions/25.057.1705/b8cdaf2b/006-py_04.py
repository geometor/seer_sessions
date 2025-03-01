"""
1.  **Identify the top row and bottom row of the input grid.**
2.  **Examine the bottom row.**
    *   **If the bottom row contains any non-white (non-0) values:**
        *   Change all white (0) cells in the top row to yellow (4).
        * other cells in the top row are unchanged.
    *   **Otherwise (if the bottom row contains only white values):**
        * The top row remains unchanged
3.  **All other rows remain unchanged.**
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""

    output_grid = np.copy(input_grid)  # Initialize output as a copy of input
    num_rows = input_grid.shape[0]
    num_cols = input_grid.shape[1]

    # Check if the bottom row has any non-white values
    bottom_row_has_non_white = any(input_grid[num_rows - 1, col] != 0 for col in range(num_cols))

    # Iterate through each cell of the top row
    for col in range(num_cols):
        if bottom_row_has_non_white:
            #if the cell is white change to yellow
            if output_grid[0,col] == 0:
                output_grid[0, col] = 4
            # output_grid[0, col] remains unchanged if not 0
        #else top row remains unchanged

    return output_grid