"""
Transforms an input sequence of 12 integers by performing a left circular rotation by 2 positions. The elements originally at indices 0 and 1 are moved to indices 10 and 11, respectively, and all other elements shift two positions to the left.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies a left circular rotation by 2 positions to the input NumPy array.

    Args:
        input_grid: A 1D NumPy array of integers (shape (12,)).

    Returns:
        A 1D NumPy array representing the transformed sequence.
    """

    # Define the amount of left circular shift required.
    rotation_amount = 2

    # Perform the left circular rotation using numpy.roll.
    # A negative shift value indicates a left rotation.
    output_grid = np.roll(input_grid, -rotation_amount)

    # Return the rotated array.
    return output_grid