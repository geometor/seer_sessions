"""
Performs a cyclic shift (rotation) of all elements in the input 1D NumPy array 
one position to the right. The element originally at the last index moves to 
the first index (index 0), and every other element moves one position to its right.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    # Performs a cyclic right shift by 1 position using numpy.roll
    # np.roll shifts elements along a given axis (default is the flattened array).
    # A positive shift value (shift=1) shifts elements to the right.
    # The last element wraps around to the beginning.
    # Handle potential edge cases like empty or single-element arrays implicitly handled by np.roll returning the original/copy.
    output_grid = np.roll(input_grid, shift=1)

    # Return the resulting shifted array
    return output_grid