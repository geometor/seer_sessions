"""
Transforms an input grid by cyclically shifting its rows downwards by one position.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid by performing a one-step downward cyclic shift on its rows.

    Args:
        input_grid: A 3x3 numpy array representing the input grid.

    Returns:
        A 3x3 numpy array representing the transformed grid.
    """
    # Initialize the output grid as a copy of the input grid.  While not
    # strictly necessary for this simple row shift, it's generally good practice
    # to avoid modifying the input in place.
    output_grid = np.copy(input_grid)

    # Perform the cyclic shift of rows.
    output_grid[0, :] = input_grid[2, :]  # Input row 2 -> Output row 0
    output_grid[1, :] = input_grid[0, :]  # Input row 0 -> Output row 1
    output_grid[2, :] = input_grid[1, :]  # Input row 1 -> Output row 2

    return output_grid