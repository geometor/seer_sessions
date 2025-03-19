"""
1.  **Identify Zero Rows:** Find all rows in the input grid that consist entirely of zeros.
2.  **Remove a Zero Row:** If any zero rows are found, remove the *first* one that appears, from top to bottom.
3.  **Output:** Return the modified grid. If no zero rows are found, return the original input grid.
"""

import numpy as np

def find_zero_rows(grid):
    """Finds the indices of all rows that contain only zeros."""
    return np.where(~grid.any(axis=1))[0]

def remove_row(grid, row_index):
    """Removes a row from the grid."""
    return np.delete(grid, row_index, axis=0)

def transform(input_grid):
    # Find all rows containing only zeros.
    zero_rows = find_zero_rows(input_grid)

    # If zero rows exist, remove the first one.
    if len(zero_rows) > 0:
        output_grid = remove_row(input_grid, zero_rows[0])
    else:
        output_grid = input_grid.copy()  # No zero rows, return input as is

    return output_grid