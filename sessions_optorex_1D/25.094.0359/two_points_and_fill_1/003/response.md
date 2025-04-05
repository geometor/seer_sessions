```python
import math # Although math isn't strictly needed here, it's included as per template instructions
import copy # Used for creating a mutable copy of the input

"""
Identifies the single non-zero digit ('fill_value') present exactly twice in the input list. 
Fills the elements between the first and second occurrences of the 'fill_value' with the 'fill_value' itself. 
Elements outside this range remain unchanged. The input is assumed to be a list or list-like structure (e.g., NumPy array) of integers.
"""

def find_first(lst, value):
    """Helper function to find the first index of a value in a list."""
    for i, x in enumerate(lst):
        if x == value:
            return i
    return -1 # Should not happen based on problem description

def find_last(lst, value):
    """Helper function to find the last index of a value in a list."""
    # Iterate backwards to find the last occurrence efficiently
    for i in range(len(lst) - 1, -1, -1):
        if lst[i] == value:
            return i
    return -1 # Should not happen based on problem description

def transform(input_list):
    """
    Transforms the input list by filling elements between the two occurrences 
    of a unique non-zero digit with that digit.

    Args:
        input_list: A list or list-like structure of integers.

    Returns:
        A new list with the transformation applied.
    """
    # Ensure we are working with a standard Python list if input is array-like
    # and create a mutable copy for the output.
    # Using deepcopy handles potential nested structures, although simple list() or copy.copy()
    # would work for a flat list of ints. Using copy.deepcopy for robustness.
    output_list = copy.deepcopy(list(input_list)) 

    # 1. Identify the non-zero integer (fill_value).
    # Based on the problem description, there's exactly one unique non-zero value.
    fill_value = 0
    for x in output_list: # Iterate through the list to find the first non-zero
        if x != 0:
            fill_value = x
            break # Found the fill value, no need to continue search

    # Handle edge case: if no non-zero value found (not expected from examples)
    if fill_value == 0:
        return output_list # Return the original list copy

    # 2. Find the index of the first occurrence (idx1).
    idx1 = find_first(output_list, fill_value)

    # 3. Find the index of the last occurrence (idx2).
    idx2 = find_last(output_list, fill_value)

    # 4. Iterate through the indices i from idx1 + 1 up to (but not including) idx2.
    # 5. For each index i in this range, set the element at index i in the output list to the fill_value.
    # Check if both indices were found and idx1 is before idx2 (as expected)
    if idx1 != -1 and idx2 != -1 and idx1 < idx2:
        for i in range(idx1 + 1, idx2):
            output_list[i] = fill_value

    # 6. Return the modified output list.
    return output_list
```