"""
Transforms an input 1D numpy array of integers by performing a left cyclic shift by 3 positions.
The first 3 elements are moved to the end of the array, preserving their relative order,
and the remaining elements are shifted 3 positions to the left.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Performs a left cyclic shift by 3 positions on a 1D numpy array.

    Args:
        input_grid: A 1-dimensional numpy array of integers.

    Returns:
        A 1-dimensional numpy array representing the transformed sequence.
    """

    # Define the amount of shift
    shift_amount = 3

    # Perform the left cyclic shift using numpy.roll.
    # A negative shift value indicates a left shift.
    output_grid = np.roll(input_grid, -shift_amount)

    # Return the resulting shifted array
    return output_grid
