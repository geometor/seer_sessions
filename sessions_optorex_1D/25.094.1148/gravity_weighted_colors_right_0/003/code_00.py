"""
Takes an input NumPy array of integers (0, 1, or 2), sorts the elements 
in descending order (2s first, then 1s, then 0s), and returns the 
sorted array.
"""

import numpy as np

def transform(input_arr: np.ndarray) -> np.ndarray:
    """
    Sorts the elements of the input NumPy array in descending order.

    Args:
        input_arr: A 1-dimensional NumPy array containing integers (0, 1, or 2).

    Returns:
        A 1-dimensional NumPy array containing the same elements as the input,
        sorted in descending order.
    """
    # 1. Sort the input array in ascending order using numpy.sort
    #    numpy.sort returns a *new* sorted array, leaving the original unchanged.
    sorted_ascending = np.sort(input_arr)

    # 2. Reverse the sorted array to achieve descending order.
    #    Slicing with [::-1] is an efficient way to reverse a NumPy array.
    sorted_descending = sorted_ascending[::-1]

    # 3. Return the resulting array sorted in descending order.
    output_arr = sorted_descending
    
    return output_arr
