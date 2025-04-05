"""
Transforms a 1D sequence of 12 elements by applying a circular right 
shift of 3 positions. The last 3 elements of the input sequence become the 
first 3 elements of the output sequence, and the first 9 elements of the input 
sequence follow them, maintaining their relative internal order.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies a circular right shift of 3 positions to the input array.

    Args:
        input_grid: A 1D NumPy array of shape (12,) containing elements (digits in this case).

    Returns:
        A 1D NumPy array of shape (12,) representing the transformed sequence.
    """

    # Define the shift amount
    shift_amount = 3

    # Perform a circular shift to the right by the specified amount
    # np.roll shifts elements along the specified axis (default is flattened array)
    # Positive shift corresponds to a right shift
    output_grid = np.roll(input_grid, shift=shift_amount)

    # Return the resulting shifted array
    return output_grid