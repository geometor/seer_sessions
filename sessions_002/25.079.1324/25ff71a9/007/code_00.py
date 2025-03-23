"""
Iterate through each row of the input grid. If a row is non-empty and not the last row, shift it down by one position, replacing the original row with an empty row.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid by shifting down non-empty rows."""
    output_grid = np.copy(input_grid)
    num_rows = output_grid.shape[0]

    # Iterate through rows from top to bottom
    for i in range(num_rows - 1):  # Iterate only up to the second-to-last row
        # Check if the current row is non-empty
        if np.any(output_grid[i] != 0):
            # Shift the row down by one
            output_grid[i+1] = output_grid[i]
            output_grid[i] = 0

    return output_grid