import numpy as np

"""
Transformation Rule: Given a sequence of digits (as a NumPy array), find the index 'i' of the first non-zero digit. If no non-zero digit exists, return the sequence unchanged. Otherwise, create a new sequence where the element at index 'i' is set to 0, and the elements from index 'i' to the second-to-last element of the original sequence are shifted one position to the right (occupying indices i+1 onwards in the new sequence). Elements before index 'i' remain the same. The last element of the original sequence is effectively discarded in the shifted case.
"""

def find_first_non_zero_index(arr: np.ndarray) -> int:
    """
    Finds the index of the first non-zero element in a 1D numpy array.

    Args:
        arr: The input 1D NumPy array.

    Returns:
        The index of the first non-zero element, or -1 if all elements are zero.
    """
    # np.nonzero returns a tuple of arrays, one for each dimension.
    # For a 1D array, we access the first element of the tuple.
    non_zero_indices = np.nonzero(arr)[0]
    if non_zero_indices.size > 0:
        # Return the first index found
        return non_zero_indices[0]
    else:
        # Indicate no non-zero element found
        return -1

def transform(input_arr: np.ndarray) -> np.ndarray:
    """
    Transforms the input numpy array by finding the first non-zero element,
    setting it to zero, and right-shifting subsequent elements.

    Args:
        input_arr: A 1D NumPy array of digits.

    Returns:
        A new 1D NumPy array representing the transformed sequence.
    """
    
    # Find the index of the first non-zero element
    first_nz_index = find_first_non_zero_index(input_arr)

    # If all elements are zero (or array is empty), return a copy unchanged
    if first_nz_index == -1 or input_arr.size == 0:
        return np.copy(input_arr) 

    # Initialize the output array as a copy of the input
    output_arr = np.copy(input_arr)
    n = len(input_arr)

    # Set the element at the first non-zero index to 0
    output_arr[first_nz_index] = 0

    # Shift the elements from the original array starting at first_nz_index
    # up to the second-to-last element, into the output array starting 
    # at index first_nz_index + 1.
    # Check if there are elements to the right of the first non-zero index to shift.
    if first_nz_index < n - 1:
        # Slice from input: input_arr[first_nz_index] to input_arr[n-2]
        # Slice into output: output_arr[first_nz_index + 1] to output_arr[n-1]
        output_arr[first_nz_index + 1 : n] = input_arr[first_nz_index : n - 1]

    return output_arr