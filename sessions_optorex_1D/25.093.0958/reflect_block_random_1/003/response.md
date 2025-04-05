```python
import numpy as np
import math # Although not used in the final code, included as per template allowance

"""
Reverses the sub-sequence of digits located between the first and last
non-zero digits in the input sequence, leaving any leading and trailing
zeros in their original positions. If the sequence contains only zeros,
it remains unchanged.
"""

def _find_first_non_zero_index(data_list):
    """Finds the index of the first non-zero element."""
    for i, val in enumerate(data_list):
        if val != 0:
            return i
    return -1 # Return -1 if all are zeros or list is empty

def _find_last_non_zero_index(data_list):
    """Finds the index of the last non-zero element."""
    n = len(data_list)
    for i in range(n - 1, -1, -1):
        if data_list[i] != 0:
            return i
    return -1 # Return -1 if all are zeros or list is empty

def transform(input_data):
    """
    Applies the transformation rule to the input data.

    Args:
        input_data: A list or numpy array of integers.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # Ensure input is a list for consistent processing
    if isinstance(input_data, np.ndarray):
        input_list = input_data.tolist()
    else:
        # Assume it's already list-like or directly usable as a list
        input_list = list(input_data)

    # Handle empty list case
    if not input_list:
        return []

    # Find the index of the first non-zero digit.
    start_index = _find_first_non_zero_index(input_list)

    # If no non-zero digits are found (all zeros), return the original list.
    if start_index == -1:
        return input_list # Return a copy or the original list

    # Find the index of the last non-zero digit.
    # Since we know there's at least one non-zero digit, this will also find an index.
    end_index = _find_last_non_zero_index(input_list)

    # Extract the prefix (leading zeros before start_index).
    prefix = input_list[:start_index]

    # Extract the middle segment (from start_index to end_index, inclusive).
    middle = input_list[start_index : end_index + 1]

    # Extract the suffix (trailing zeros after end_index).
    suffix = input_list[end_index + 1:]

    # Reverse the middle segment.
    reversed_middle = middle[::-1]

    # Concatenate the prefix, reversed middle segment, and suffix.
    output_list = prefix + reversed_middle + suffix

    # Return the transformed list
    return output_list
```