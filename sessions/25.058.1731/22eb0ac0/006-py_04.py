"""
1.  **Identify the Special Row:** The special row is always the row at index 1 (the second row) of the input grid.
2.  **Find the leftmost non-zero color**: Find the leftmost non-zero pixel in the special row. This pixel's color will be used to fill the special row.
3.  **Fill the Special Row:** Fill the entire special row (row index 1) of the *output* grid with the color found in step 2.
4.  **Copy Other Rows:** All other rows in the output grid are identical to the corresponding rows in the input grid.
"""

import numpy as np

def get_leftmost_nonzero(row):
    """Finds the leftmost non-zero element in a row."""
    for pixel in row:
        if pixel != 0:
            return pixel
    return 0  # Should not happen in the given examples, but handle for completeness

def transform(input_grid):
    # initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # get special_row (always index 1)
    special_row_index = 1
    special_row = input_grid[special_row_index]

    # Find the leftmost non-zero color
    replacement_color = get_leftmost_nonzero(special_row)

    # Fill the special row in output
    output_grid[special_row_index] = np.full(len(special_row), replacement_color)
    
    return output_grid