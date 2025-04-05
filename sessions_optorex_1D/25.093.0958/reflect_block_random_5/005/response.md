```python
import numpy as np

"""
Reverses the contiguous sub-sequence of non-zero digits within a sequence (list or numpy array) of digits, leaving any leading or trailing zeros in their original positions.

1.  Receive the input sequence of digits (e.g., as a list or NumPy array).
2.  Find the index of the first non-zero digit in the sequence. If no non-zero digits exist, return the original sequence unchanged.
3.  Find the index of the last non-zero digit in the sequence.
4.  Extract the sub-sequence of leading zeros (all elements *before* the first non-zero index). This may be empty.
5.  Extract the sub-sequence containing all elements from the first non-zero index up to and including the last non-zero index (the "non-zero segment").
6.  Extract the sub-sequence of trailing zeros (all elements *after* the last non-zero index). This may be empty.
7.  Reverse the order of the elements within the extracted "non-zero segment".
8.  Construct the final output sequence by concatenating the leading zeros, the reversed non-zero segment, and the trailing zeros, in that specific order.
9.  Return the constructed output sequence.
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
        input_grid (np.ndarray): A 1D NumPy array of integers representing the sequence.

    Returns:
        np.ndarray: The transformed 1D NumPy array.
    """

    # Ensure input is a NumPy array (might be passed as a list)
    if not isinstance(input_grid, np.ndarray):
        input_grid_np = np.array(input_grid)
    else:
        input_grid_np = input_grid

    # Step 2 & 3: Find the indices of the first and last non-zero elements
    start_index = find_first_nonzero_index_np(input_grid_np)

    # Handle the edge case where the sequence contains only zeros
    if start_index == -1:
        # Return a copy of the original sequence/array
        return input_grid_np.copy()

    end_index = find_last_nonzero_index_np(input_grid_np)

    # Step 4, 5, 6: Extract the three parts: leading zeros, non-zero segment, trailing zeros
    leading_zeros = input_grid_np[:start_index]
    non_zero_segment = input_grid_np[start_index : end_index + 1]
    trailing_zeros = input_grid_np[end_index + 1 :]

    # Step 7: Reverse the non-zero segment
    # Slicing [::-1] works efficiently for reversing NumPy arrays
    reversed_segment = non_zero_segment[::-1]

    # Step 8: Reconstruct the sequence using NumPy concatenation
    # Ensure all parts are NumPy arrays before concatenating (they already are due to slicing)
    output_grid = np.concatenate((leading_zeros, reversed_segment, trailing_zeros))

    # Step 9: Return the result
    return output_grid
```