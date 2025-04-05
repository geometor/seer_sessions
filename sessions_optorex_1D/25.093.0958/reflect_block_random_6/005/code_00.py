import numpy as np
import math

"""
Reverses the contiguous subsequence of a 1D NumPy array that starts at the first 
non-zero element and ends at the last non-zero element. Leading and trailing 
zeros outside this subsequence remain in their original positions.
"""

def _find_first_last_nonzero_indices(arr: np.ndarray):
    """
    Finds the indices of the first and last non-zero elements in a 1D array.

    Args:
        arr: The input 1D NumPy array.

    Returns:
        A tuple (start_index, end_index). Returns (None, None) if no non-zero
        elements are found.
    """
    # Find indices of all non-zero elements
    non_zero_indices = np.nonzero(arr)[0] 
    
    # Handle case where there are no non-zero elements
    if len(non_zero_indices) == 0:
        return None, None 
    
    # The first non-zero index is the minimum of the found indices
    start_index = non_zero_indices[0]
    # The last non-zero index is the maximum of the found indices
    end_index = non_zero_indices[-1]
    
    return start_index, end_index

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Reverses the subsequence of non-zero elements within a 1D NumPy array,
    preserving leading and trailing zeros.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A 1D NumPy array with the non-zero subsequence reversed.
    """

    # 1. Find the index of the first and last non-zero elements.
    start_index, end_index = _find_first_last_nonzero_indices(input_grid)

    # 2. If there are no non-zero elements, return the original input array.
    if start_index is None:
        # Return a copy to avoid modifying the original if it was passed by reference
        return input_grid.copy() 

    # 3. Extract three parts of the array:
    #    a. Leading zeros slice (elements before the first non-zero)
    leading_zeros = input_grid[:start_index]
    
    #    b. Subsequence slice (elements from first non-zero up to and including last non-zero)
    #       Note: Slicing up to end_index + 1 includes the element at end_index.
    subsequence = input_grid[start_index : end_index + 1]
    
    #    c. Trailing zeros slice (elements after the last non-zero)
    trailing_zeros = input_grid[end_index + 1 :]

    # 4. Reverse the subsequence slice.
    reversed_subsequence = subsequence[::-1] # Standard Python slicing for reversal

    # 5. Construct the output array by concatenating the slices.
    #    np.concatenate handles potentially empty leading/trailing zero arrays correctly.
    output_grid = np.concatenate((leading_zeros, reversed_subsequence, trailing_zeros))

    # 6. Return the constructed output array.
    return output_grid