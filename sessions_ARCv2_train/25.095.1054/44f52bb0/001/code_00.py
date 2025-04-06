"""
Checks if a 3x3 grid containing 0s and 2s is vertically symmetric.
If the first column is identical to the third column, output 1.
Otherwise, output 7.
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> int:
    """
    Checks for vertical symmetry in a 3x3 grid.

    Args:
        input_grid: A 3x3 list of lists representing the input grid.

    Returns:
        1 if the grid is vertically symmetric (first column equals third column),
        7 otherwise.
    """

    # Convert the input list of lists to a NumPy array for easier column access
    grid = np.array(input_grid)

    # Extract the first and third columns
    first_column = grid[:, 0]
    third_column = grid[:, 2]

    # Check if the first column is identical to the third column
    is_symmetric = np.array_equal(first_column, third_column)

    # Determine the output based on symmetry
    if is_symmetric:
        output = 1
    else:
        output = 7

    return output
