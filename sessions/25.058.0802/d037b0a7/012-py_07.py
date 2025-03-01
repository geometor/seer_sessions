"""
Copies the entire second row of the input grid to the last row of the output grid. The dimensions of the output grid are the same as the input, and all other rows remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.  This ensures
    # that all rows except the last row will remain the same.
    output_grid = np.copy(input_grid)

    # Get the number of rows in the input grid.
    num_rows = input_grid.shape[0]

    # Check if the input grid has at least two rows.  If not, there's no second
    # row to copy, so return the unchanged copy.
    if num_rows < 2:
        return output_grid

    # Copy the second row (index 1) of the input grid to the last row (index -1)
    # of the output grid.
    output_grid[-1, :] = input_grid[1, :]

    return output_grid