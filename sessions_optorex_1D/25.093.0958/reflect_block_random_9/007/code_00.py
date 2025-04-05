"""
Reverses the contiguous sub-sequence of non-zero digits within a NumPy array, 
leaving any leading or trailing zeros in their original positions. 
Handles arrays containing only zeros by returning an identical array.
"""

import numpy as np

def find_first_non_zero_index(arr: np.ndarray) -> int:
    """
    Finds the index of the first non-zero element in a NumPy array.
    Returns -1 if no non-zero element is found.
    """
    indices = np.nonzero(arr)[0] # Get indices of non-zero elements
    if indices.size > 0:
        return indices[0]
    else:
        return -1 # No non-zero elements found

def find_last_non_zero_index(arr: np.ndarray) -> int:
    """
    Finds the index of the last non-zero element in a NumPy array.
    Assumes at least one non-zero element exists (caller should check first).
    Returns -1 if no non-zero element is found (for completeness, though might not be reached in typical flow).
    """
    indices = np.nonzero(arr)[0] # Get indices of non-zero elements
    if indices.size > 0:
        return indices[-1]
    else:
        return -1 # Should not be reached if find_first_non_zero_index didn't return -1

def transform(input_array: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.

    Workflow:
    1. Find the index of the first non-zero element (`start_index`).
    2. Handle the edge case: If no non-zero elements are found (`start_index == -1`), return a copy of the original array.
    3. Find the index of the last non-zero element (`end_index`).
    4. Slice the input array to extract the leading zeros part (before `start_index`).
    5. Slice the input array to extract the non-zero block (from `start_index` to `end_index` inclusive).
    6. Slice the input array to extract the trailing zeros part (after `end_index`).
    7. Reverse the extracted non-zero block using NumPy slicing.
    8. Concatenate the leading zeros, reversed non-zero block, and trailing zeros parts using np.concatenate.
    9. Return the reconstructed NumPy array.
    """
    # 1. Find the index of the first non-zero element.
    start_index = find_first_non_zero_index(input_array)

    # 2. Handle the edge case: All zeros or empty array.
    if start_index == -1:
        return input_array.copy() # Return a copy to avoid modifying the original if it's mutable

    # 3. Find the index of the last non-zero element.
    #    (We know at least one exists if start_index != -1)
    end_index = find_last_non_zero_index(input_array)

    # 4. Slice to get leading zeros.
    leading_zeros = input_array[:start_index]

    # 5. Slice to get the non-zero block.
    non_zero_block = input_array[start_index : end_index + 1]

    # 6. Slice to get trailing zeros.
    trailing_zeros = input_array[end_index + 1:]

    # 7. Reverse the non-zero block.
    reversed_non_zero_block = non_zero_block[::-1]

    # 8. Concatenate the parts.
    # Ensure all parts are arrays for concatenation. Slicing NumPy arrays returns views or copies which are arrays.
    output_array = np.concatenate((leading_zeros, reversed_non_zero_block, trailing_zeros))

    # 9. Return the reconstructed array.
    return output_array