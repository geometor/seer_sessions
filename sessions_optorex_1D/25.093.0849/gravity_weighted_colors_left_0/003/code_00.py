"""
Sorts the elements of the input sequence (represented as a NumPy array) in ascending numerical order.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input numpy array by sorting its elements numerically.

    Args:
        input_grid: A numpy array containing integers (0, 1, 2).

    Returns:
        A numpy array containing the sorted integers.
    """
    # Sort the elements of the input numpy array in ascending order
    output_grid = np.sort(input_grid)

    # Return the sorted array
    return output_grid
