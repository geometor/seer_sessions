"""
Performs a left circular shift on the input sequence by moving the first element to the end.
"""

import numpy as np
import collections # Keep collections import for potential alternative approaches if needed

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Takes a 1D NumPy array of integers and performs a left circular shift by one position.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A new 1D NumPy array representing the input array after the shift.
    """

    # Get the size of the input array
    size = input_grid.shape[0]

    # Handle edge cases: empty or single-element arrays remain unchanged.
    # np.roll handles these cases correctly (returns a copy), so explicit checks
    # are not strictly necessary but can be added for clarity if desired.
    if size <= 1:
        return input_grid.copy() 

    # Perform a left circular shift by 1 position using np.roll.
    # A negative shift value indicates a left shift.
    output_grid = np.roll(input_grid, shift=-1)

    return output_grid