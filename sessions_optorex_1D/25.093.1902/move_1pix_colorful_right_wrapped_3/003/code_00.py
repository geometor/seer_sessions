"""
Performs a right circular shift (rotation) on the input 1D NumPy array by one position.
The last element wraps around to become the first element.
"""

import numpy as np

def transform(input_array: np.ndarray) -> np.ndarray:
    """
    Performs a right circular shift on a 1D NumPy array by one position.

    Args:
        input_array: A 1-dimensional NumPy array of shape (12,) containing integers.

    Returns:
        A 1-dimensional NumPy array of shape (12,) representing the input array
        rotated one position to the right.
    """
    # Check if the input array is empty or None to avoid errors
    if input_array is None or input_array.size == 0:
        # Depending on requirements, might return None, empty array, or raise error
        return np.array([], dtype=input_array.dtype) # Return empty array of same type

    # Use numpy.roll to perform the right circular shift by 1 position
    # The 'shift' argument is positive for a right shift
    output_array = np.roll(input_array, shift=1)

    # Return the resulting array
    return output_array
