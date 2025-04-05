import numpy as np

"""
Reverses the contiguous sub-sequence of non-zero digits within a sequence (list or numpy array) of digits, leaving any leading or trailing zeros in their original positions.

1.  Receive the input sequence of digits (e.g., as a list or NumPy array).
2.  Convert the input to a NumPy array if it isn't already.
3.  Find the index of the first non-zero digit (`start_index`) in the array.
4.  If no non-zero digit is found (`start_index` is -1), return a copy of the original input array.
5.  Find the index of the last non-zero digit (`end_index`) in the array.
6.  Extract the sub-array of leading zeros (elements before `start_index`).
7.  Extract the sub-array representing the non-zero segment (elements from `start_index` to `end_index`, inclusive).
8.  Extract the sub-array of trailing zeros (elements after `end_index`).
9.  Reverse the order of elements within the extracted non-zero segment sub-array.
10. Construct the output array by concatenating the leading zeros sub-array, the reversed non-zero segment sub-array, and the trailing zeros sub-array in that order.
11. Return the constructed output array.
"""


def find_first_nonzero_index_np(arr):
    """Finds the index of the first non-zero element in a NumPy array."""
    indices = np.where(arr != 0)[0]
    # Return the first index if found, otherwise return -1
    if len(indices) == 0:
        return -1
    return indices[0]

def find_last_nonzero_index_np(arr):
    """Finds the index of the last non-zero element in a NumPy array."""
    indices = np.where(arr != 0)[0]
    # Return the last index if found, otherwise return -1
    if len(indices) == 0:
        return -1
    return indices[-1]

def transform(input_grid):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_grid (np.ndarray or list): A 1D sequence of integers.

    Returns:
        np.ndarray: The transformed 1D NumPy array.
    """

    # Step 2: Ensure input is a NumPy array
    if not isinstance(input_grid, np.ndarray):
        input_grid_np = np.array(input_grid)
    else:
        input_grid_np = input_grid

    # Step 3: Find the index of the first non-zero element
    start_index = find_first_nonzero_index_np(input_grid_np)

    # Step 4: Handle the edge case where the sequence contains only zeros
    if start_index == -1:
        # Return a copy of the original sequence/array
        return input_grid_np.copy()

    # Step 5: Find the index of the last non-zero element
    end_index = find_last_nonzero_index_np(input_grid_np)

    # Step 6: Extract the leading zeros sub-array
    leading_zeros = input_grid_np[:start_index]

    # Step 7: Extract the non-zero segment sub-array
    non_zero_segment = input_grid_np[start_index : end_index + 1]

    # Step 8: Extract the trailing zeros sub-array
    trailing_zeros = input_grid_np[end_index + 1 :]

    # Step 9: Reverse the non-zero segment
    reversed_segment = non_zero_segment[::-1] # Efficient NumPy slicing for reversal

    # Step 10: Reconstruct the sequence using NumPy concatenation
    output_grid = np.concatenate((leading_zeros, reversed_segment, trailing_zeros))

    # Step 11: Return the result
    return output_grid