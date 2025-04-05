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
    non_zero_indices = np.nonzero(arr)[0] # Get indices of non-zero elements
    if len(non_zero_indices) == 0:
        return None, None # No non-zero elements found
    
    start_index = non_zero_indices[0]
    end_index = non_zero_indices[-1]
    return start_index, end_index

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Reverses the subsequence of non-zero elements within a 1D NumPy array.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A 1D NumPy array with the non-zero subsequence reversed, 
        preserving leading/trailing zeros.
    """
    # 1. Receive the input 1D NumPy array (already done via input_grid).
    
    # 2 & 4. Find the index of the first and last non-zero elements.
    start_index, end_index = _find_first_last_nonzero_indices(input_grid)

    # 3. If there are no non-zero elements, return the original input array.
    if start_index is None:
        return input_grid.copy() # Return a copy to avoid modifying the original if passed by reference

    # 5. Extract three parts of the array:
    #    a. Leading zeros slice
    leading_zeros = input_grid[:start_index]
    
    #    b. Subsequence slice (inclusive of end_index)
    subsequence = input_grid[start_index : end_index + 1]
    
    #    c. Trailing zeros slice
    trailing_zeros = input_grid[end_index + 1 :]

    # 6. Reverse the subsequence slice.
    reversed_subsequence = subsequence[::-1]

    # 7. Construct the output array by concatenating the slices.
    # Use np.concatenate which handles empty arrays correctly.
    output_grid = np.concatenate((leading_zeros, reversed_subsequence, trailing_zeros))

    # 8. Return the constructed output array.
    return output_grid