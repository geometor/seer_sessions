"""
The transformation removes the rightmost column and the bottom row from the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by removing the rightmost column and bottom row.
    """
    # Create a copy of the input grid to avoid modifying the original.
    output_grid = np.copy(input_grid)

    # Remove the last row.
    output_grid = output_grid[:-1, :]

    # Remove the rightmost column.
    output_grid = output_grid[:, :-1]

    return output_grid