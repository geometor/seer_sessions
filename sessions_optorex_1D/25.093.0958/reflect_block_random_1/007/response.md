```python
import numpy as np # Although numpy isn't strictly necessary for list manipulation, it's often available.
import math # Included as per template allowance, though not used here.

"""
Reverses the sub-sequence of digits located between the first and last
non-zero digits in the input sequence, leaving any leading and trailing
zeros in their original positions. If the sequence contains only zeros,
it remains unchanged.
"""

def _find_first_non_zero_index(data_list):
    """
    Helper function to find the index of the first non-zero element in a list.
    Returns -1 if no non-zero element is found or the list is empty.
    """
    for i, val in enumerate(data_list):
        if val != 0:
            return i
    return -1 # Return -1 if all are zeros or list is empty

def _find_last_non_zero_index(data_list):
    """
    Helper function to find the index of the last non-zero element in a list.
    Returns -1 if no non-zero element is found or the list is empty.
    """
    n = len(data_list)
    for i in range(n - 1, -1, -1):
        if data_list[i] != 0:
            return i
    return -1 # Return -1 if all are zeros or list is empty

def transform(input_list):
    """
    Applies the transformation rule to the input list of integers.

    Args:
        input_list: A list of integers representing the sequence.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # Create a working copy to avoid modifying the original input list if it's mutable
    work_list = list(input_list)

    # Handle empty list case - return empty list
    if not work_list:
        return []

    # 1. Determine the index of the first non-zero element
    start_index = _find_first_non_zero_index(work_list)

    # 2. If no non-zero element is found (all zeros), return the original list unchanged.
    if start_index == -1:
        return work_list # Return the copy

    # 3. Determine the index of the last non-zero element.
    #    (We know at least one non-zero exists, so this will find an index >= start_index)
    end_index = _find_last_non_zero_index(work_list)

    # 4. Extract the prefix sub-sequence (leading zeros).
    prefix = work_list[:start_index]

    # 5. Extract the core sub-sequence (from first to last non-zero, inclusive).
    core = work_list[start_index : end_index + 1]

    # 6. Extract the suffix sub-sequence (trailing zeros).
    suffix = work_list[end_index + 1:]

    # 7. Reverse the order of the elements within the core sub-sequence.
    reversed_core = core[::-1] # Pythonic way to reverse a list

    # 8. Construct the final output sequence by concatenating the parts.
    output_list = prefix + reversed_core + suffix

    # 9. Return the constructed output list.
    return output_list
```