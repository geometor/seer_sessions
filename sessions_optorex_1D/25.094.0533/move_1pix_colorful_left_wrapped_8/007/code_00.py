"""
Performs a single left circular shift on the input sequence (1D NumPy array). The first element is moved to the last position, and all other elements shift one position to the left.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Performs a left circular shift on a 1D NumPy array.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A 1D NumPy array representing the sequence after the first element
        has been moved to the end.
    """

    # Get the size of the input array
    size = input_grid.size

    # Handle edge cases: empty or single-element array, return a copy
    if size <= 1:
        return input_grid.copy()

    # Perform the left circular shift using numpy.roll
    # A shift of -1 moves elements to the left, wrapping the first element to the end.
    output_grid = np.roll(input_grid, -1)

    # The output_grid now holds the transformed sequence
    return output_grid
