"""
Transforms an input sequence of 12 integers by performing a right rotation by one position.
The last element of the input sequence is moved to the beginning, and all other elements
are shifted one position to the right.
"""

import numpy as np

def transform(input_sequence: np.ndarray) -> np.ndarray:
    """
    Performs a right rotation by one position on a sequence of integers.

    Args:
        input_sequence: A NumPy array containing 12 integers.

    Returns:
        A NumPy array containing the transformed sequence of 12 integers.
    """

    # Ensure the input is a numpy array (it might be passed as a list)
    if not isinstance(input_sequence, np.ndarray):
        input_sequence = np.array(input_sequence)

    # Check if the sequence is empty or has only one element, rotation has no effect
    if input_sequence.size <= 1:
        return input_sequence.copy() # Return a copy to avoid modifying the original if passed by reference

    # Perform right rotation by 1 position using numpy.roll
    # np.roll(array, shift, axis=None)
    # A positive shift value corresponds to a right rotation
    output_sequence = np.roll(input_sequence, 1)

    return output_sequence
