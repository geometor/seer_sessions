"""
Transforms an input NumPy array of integers by moving all zero elements to the 
beginning while preserving the relative order of the non-zero elements.
"""

import numpy as np

def filter_zeros(input_array):
    """Filters out the zero elements from the input array."""
    # Use boolean indexing to select elements equal to 0
    return input_array[input_array == 0]

def filter_non_zeros(input_array):
    """Filters out the non-zero elements from the input array, preserving order."""
    # Use boolean indexing to select elements not equal to 0
    return input_array[input_array != 0]

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Moves all zeros in a 1D NumPy array to the front, preserving the relative
    order of non-zero elements.

    Args:
        input_grid: A 1D NumPy array containing integers.

    Returns:
        A 1D NumPy array with zeros moved to the front and non-zeros
        following in their original relative order.
    """
    # Filter out the zero elements
    zeros = filter_zeros(input_grid)

    # Filter out the non-zero elements, preserving their relative order
    non_zeros = filter_non_zeros(input_grid)

    # Concatenate the array of zeros and the array of non-zeros
    output_grid = np.concatenate((zeros, non_zeros))

    # Return the transformed array
    return output_grid
