"""
Transforms an input sequence of 12 digits (represented as a NumPy array) 
by performing a single left circular shift. The first digit moves to the 
last position, and all other digits shift one position to the left.
"""

import numpy as np

def transform(input_sequence: np.ndarray) -> np.ndarray:
    """
    Performs a left circular shift on a sequence of digits represented as a NumPy array.

    Args:
        input_sequence: A 1D NumPy array representing the input sequence of digits.

    Returns:
        A 1D NumPy array representing the output sequence after the shift.
    """

    # Define the amount to shift (negative for left shift)
    shift_amount = -1

    # Perform the left circular shift using numpy.roll
    # np.roll shifts elements along a given axis.
    # For a 1D array, it shifts elements, wrapping around the ends.
    # A negative shift value moves elements to the left.
    output_sequence = np.roll(input_sequence, shift_amount)

    # Return the transformed sequence
    return output_sequence
