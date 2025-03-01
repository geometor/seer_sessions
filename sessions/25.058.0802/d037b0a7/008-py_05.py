"""
Copies the middle row of a 3x3 input grid to the bottom row, leaving the top row unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 3x3 grid by copying the middle row to the bottom row.

    Args:
        input_grid: A 3x3 numpy array representing the input grid.

    Returns:
        A 3x3 numpy array representing the transformed grid.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Copy the middle row (index 1) to the bottom row (index 2).
    output_grid[2, :] = output_grid[1, :]

    return output_grid