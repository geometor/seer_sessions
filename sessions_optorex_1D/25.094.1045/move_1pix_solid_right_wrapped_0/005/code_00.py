"""
Transforms an input sequence of integers by finding the last non-zero element 
and moving it to the position of the first zero element, provided the last 
non-zero element's index is not already less than the first zero's index. 
If no zeros or no non-zero elements are found, or if the last non-zero 
element is already before the first zero, the original sequence is returned 
unchanged.
"""

import numpy as np # Include numpy as it might be used by the environment

def find_first_zero_index(sequence):
    """
    Finds the index of the first occurrence of the number 0 in the sequence.
    Returns -1 if 0 is not found.
    """
    for i, val in enumerate(sequence):
        if val == 0:
            return i
    return -1 # Indicate not found

def find_last_non_zero(sequence):
    """
    Finds the index and value of the last non-zero element in the sequence.
    Returns (-1, None) if no non-zero element is found.
    """
    last_non_zero_index = -1
    last_non_zero_value = None
    for i, val in enumerate(sequence):
        if val != 0:
            last_non_zero_index = i
            last_non_zero_value = val
    return last_non_zero_index, last_non_zero_value

def transform(input_grid):
    """
    Applies the transformation rule to the input sequence.
    Input is expected to be list-like (e.g., list or numpy array).
    Output will be a Python list.
    """

    # Ensure input is a standard Python list for manipulation
    # The testing environment likely handles numpy array conversion if needed
    if isinstance(input_grid, np.ndarray):
        input_list = input_grid.tolist()
    else:
        # Assume list or list-like, create a copy to avoid modifying original if it's mutable
        input_list = list(input_grid) 

    # 1. Find the index of the first zero
    first_zero_index = find_first_zero_index(input_list)

    # 2. Find the index and value of the last non-zero element
    last_non_zero_index, last_non_zero_value = find_last_non_zero(input_list)

    # 3. Check conditions for returning the original sequence unchanged
    # Condition: No zero found
    if first_zero_index == -1:
        return input_list # Return original list
    # Condition: No non-zero found
    if last_non_zero_index == -1:
        return input_list # Return original list
    # Condition: Last non-zero is already before the first zero
    if last_non_zero_index < first_zero_index:
        return input_list # Return original list

    # 4. If conditions met, perform the transformation on a copy
    # Create a mutable copy to perform operations
    output_list = list(input_list)

    # 5. Remove the last non-zero element from its original position
    # We use pop(index) to remove the element at the specific index
    # The value is already stored in last_non_zero_value
    output_list.pop(last_non_zero_index)

    # 6. Insert the removed value at the index of the first zero
    # The first_zero_index remains the correct target insertion point relative
    # to the elements *before* it, because the removed element was at an index
    # greater than or equal to first_zero_index.
    output_list.insert(first_zero_index, last_non_zero_value)

    # 7. Return the modified list
    return output_list