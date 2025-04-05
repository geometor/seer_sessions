"""
Takes an input 1D NumPy array of integers (0, 1, or 2), sorts the elements 
in descending order (2s first, then 1s, then 0s), and returns the 
sorted array.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Sorts the elements of the input 1D NumPy array in descending order.

    Args:
        input_grid: A 1-dimensional NumPy array containing integers (0, 1, or 2).

    Returns:
        A 1-dimensional NumPy array containing the same elements as the input,
        sorted in descending order (e.g., 2s first, then 1s, then 0s).
    """
    
    # 1. Sort the input array using np.sort. This sorts in ascending order by default
    #    and returns a new sorted array, leaving the input unchanged.
    sorted_ascending = np.sort(input_grid)
    
    # 2. Reverse the sorted array to achieve descending order.
    #    Slicing with [::-1] is an efficient way to reverse a NumPy array.
    #    This ensures the order is 2s, then 1s, then 0s.
    output_grid = sorted_ascending[::-1]
    
    # 3. Return the resulting array sorted in descending order.
    return output_grid
