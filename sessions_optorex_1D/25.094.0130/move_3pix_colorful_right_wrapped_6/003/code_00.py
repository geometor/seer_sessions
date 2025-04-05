"""
Perform a right circular shift (rotation) on the input 1-dimensional NumPy array of 12 integers by 3 positions.
"""

import numpy as np

def transform(input_array: np.ndarray) -> np.ndarray:
    """
    Performs a right circular shift on a 1D NumPy array by 3 positions.

    Args:
        input_array: A 1-dimensional NumPy array of 12 integers.

    Returns:
        A 1-dimensional NumPy array representing the input array rotated right by 3 positions.
    """
    # Define the amount to shift the array elements
    shift_amount = 3

    # Perform the right circular shift using numpy.roll
    # For a 1D array, the axis argument is not needed or can be None/0.
    # A positive shift value indicates a shift towards the end (right).
    output_array = np.roll(input_array, shift=shift_amount)

    # Return the resulting shifted array
    return output_array