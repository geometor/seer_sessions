"""
The transformation rule is to iterate through each row of the input grid.
If a row is not empty and is not the last row, shift it down by one position.
The row's original position is then filled with zeros.
"""

import numpy as np

def is_empty_row(row):
    """Checks if a row is empty (all zeros)."""
    return np.all(row == 0)

def shift_row_down(grid, row_index):
    """Shifts a row down by one position and fills the original position with zeros."""
    if row_index < grid.shape[0] - 1:
        grid[row_index + 1, :] = grid[row_index, :]
        grid[row_index, :] = 0
    return grid

def transform(input_grid):
    """Transforms the input grid according to the rule."""
    output_grid = np.copy(input_grid)

    # Iterate through each row of the input grid
    for i in range(output_grid.shape[0]):
        # Check if the row is not empty and is not the last row
        if not is_empty_row(output_grid[i]) and i < output_grid.shape[0] - 1:
            # Shift the row down by one position
            output_grid = shift_row_down(output_grid, i)

    return output_grid