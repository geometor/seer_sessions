```python
"""
Reverses the contiguous sub-sequence of non-zero digits within a sequence (list or numpy array) of digits, leaving any leading or trailing zeros in their original positions.
"""

import numpy as np

def find_first_nonzero_index_np(arr):
    """Finds the index of the first non-zero element in a NumPy array."""
    indices = np.where(arr != 0)[0]
    if len(indices) == 0:
        return -1
    return indices[0]

def find_last_nonzero_index_np(arr):
    """Finds the index of the last non-zero element in a NumPy array."""
    indices = np.where(arr != 0)[0]
    if len(indices) == 0:
        return -1
    return indices[-1]

def transform(input_grid):
    """
    Applies the transformation rule to the input sequence (expected as a NumPy array).

    Args:
        input_grid (np.ndarray): A 1D NumPy array of integers.

    Returns:
        np.ndarray: The transformed 1D NumPy array.
    """
    # Ensure input is a NumPy array (it might be passed as a list)
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)

    # Find the indices of the first and last non-zero elements
    start_index = find_first_nonzero_index_np(input_grid)

    # Handle the case where the sequence contains only zeros or is empty
    if start_index == -1:
        return input_grid.copy() # Return a copy of the original sequence/array

    end_index = find_last_nonzero_index_np(input_grid)

    # Extract the three parts: leading zeros, non-zero segment, trailing zeros
    leading_zeros = input_grid[:start_index]
    non_zero_segment = input_grid[start_index : end_index + 1]
    trailing_zeros = input_grid[end_index + 1 :]

    # Reverse the non-zero segment
    # Slicing [::-1] works efficiently for reversing NumPy arrays
    reversed_segment = non_zero_segment[::-1]

    # Reconstruct the sequence using NumPy concatenation
    # Ensure all parts are NumPy arrays before concatenating
    output_grid = np.concatenate((leading_zeros, reversed_segment, trailing_zeros))

    return output_grid
```