import numpy as np
import math
import re # Although re is imported, it's not used in this specific solution.

"""
The transformation rule takes a 1D NumPy array of single-digit integers as input.
It identifies the 'active subsequence' which consists of all elements from the beginning 
of the input array up to and including the last non-zero element. 
If the input array contains only zeros or has no trailing zeros, the output is 
identical to the input array.
Otherwise, the output array is constructed by repeating the 'active subsequence' 
cyclically until the output array reaches the same length as the input array.
"""

def find_last_non_zero_index(arr: np.ndarray) -> int:
    """
    Finds the index of the last non-zero element in a 1D NumPy array.
    Returns -1 if all elements are zero or the array is empty.
    
    Args:
        arr: The input 1D NumPy array.

    Returns:
        The index of the last non-zero element, or -1.
    """
    non_zero_indices = np.where(arr != 0)[0]
    if len(non_zero_indices) == 0:
        return -1
    else:
        return non_zero_indices[-1]

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input 1D NumPy array according to the described rule.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A 1D NumPy array representing the transformed sequence.
    """
    # Get the total length of the input array
    input_length = len(input_grid)

    # Handle empty input case
    if input_length == 0:
        return np.array([])

    # Find the index of the last non-zero element
    last_non_zero_idx = find_last_non_zero_index(input_grid)

    # Determine the active subsequence
    # If all elements are zeros (last_non_zero_idx is -1)
    if last_non_zero_idx == -1:
        # Input is all zeros, return a copy of the input
        return input_grid.copy()
    
    # Extract the active subsequence
    active_subsequence = input_grid[:last_non_zero_idx + 1]
    len_active = len(active_subsequence)

    # Check if there are no trailing zeros (active subsequence is the whole input)
    if len_active == input_length:
        # No trailing zeros, output is same as input, return a copy
        return input_grid.copy()

    # Initialize the output array (can use np.empty for slight performance gain if desired, but zeros_like is safer)
    output_grid = np.zeros_like(input_grid)

    # Construct the output sequence by repeating the active subsequence
    for i in range(input_length):
        # Calculate the index within the active subsequence using the modulo operator
        active_index = i % len_active
        # Assign the corresponding element to the output grid
        output_grid[i] = active_subsequence[active_index]

    return output_grid