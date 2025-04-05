import numpy as np
import math
import re # Although re isn't strictly needed for this logic, including common imports

"""
Transforms an input sequence of digits according to the following rule:
1. Convert the input sequence (provided as a 1D NumPy array) into a list of integers.
2. Find the index of the first non-zero integer in the list.
3. If no non-zero integer is found (the list contains only zeros), convert the original list back into a space-separated string and return it.
4. If a non-zero integer is found at a specific index:
   a. Create a mutable copy of the list.
   b. Insert the integer 0 into the copied list at the found index.
   c. Remove the last element from this modified list to maintain the original length.
   d. Convert the modified list back into a single string with elements separated by spaces.
   e. Return the resulting string.
"""

def _find_first_non_zero_index(data_list):
    """
    Helper function to find the index of the first non-zero element in a list.

    Args:
        data_list: A list of numbers.

    Returns:
        The index of the first non-zero element, or -1 if all elements are zero.
    """
    for index, value in enumerate(data_list):
        if value != 0:
            return index
    return -1 # Indicate no non-zero element found

def transform(input_grid: np.ndarray) -> str:
    """
    Applies the transformation rule to the input NumPy array sequence.

    Args:
        input_grid: A 1D NumPy array containing single digits (0-9).

    Returns:
        A string representing the transformed sequence with digits separated by spaces.
    """
    # 1. Convert the input NumPy array to a Python list.
    input_list = input_grid.tolist()

    # 2. Find the index of the first non-zero integer.
    first_nz_idx = _find_first_non_zero_index(input_list)

    # 3. Handle the all-zero case.
    if first_nz_idx == -1:
        # Convert the original list back to a space-separated string.
        output_str = " ".join(map(str, input_list))
        return output_str
    else:
        # 4. Handle the case where a non-zero integer is found.
        # a. Create a mutable copy of the list.
        output_list = list(input_list) # Make a copy

        # b. Insert the integer 0 into the copied list at the found index.
        output_list.insert(first_nz_idx, 0)

        # c. Remove the last element from the modified list.
        output_list.pop() # Removes the last element

        # d. Convert the modified list back into a space-separated string.
        output_str = " ".join(map(str, output_list))

        # e. Return the resulting string.
        return output_str