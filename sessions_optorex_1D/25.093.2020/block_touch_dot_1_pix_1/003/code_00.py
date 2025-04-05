import numpy as np
import math

"""
Receive the input as a list/array of integers.
Find the index of the first occurrence of the integer 2 in the input list.
If 2 is not found in the list, return the original list unchanged.
If 2 is found at index i, iterate through the list starting from index i + 1 up to the second-to-last element (index len(list) - 2).
For each element at index j in this iteration:
  a. Check if the element list[j] is 0.
  b. Check if the next element list[j + 1] is not 0.
  c. If both conditions (a and b) are true, this is the target 0. Store index j and stop iterating.
If a target 0 was found at index j:
  a. Create a mutable copy of the original list.
  b. Remove the element at index j from the copy.
  c. Append the integer 0 to the end of the copy.
  d. Return the modified list (as a numpy array).
If the iteration completes without finding a 0 followed by a non-zero digit after the first 2, return the original list unchanged.
"""

def find_first_occurrence(sequence, value):
    """Helper function to find the index of the first occurrence of a value."""
    try:
        # Convert to list if it's a numpy array to use index()
        if isinstance(sequence, np.ndarray):
            sequence_list = sequence.tolist()
        else:
            sequence_list = list(sequence) # Ensure it's a list
        return sequence_list.index(value)
    except ValueError:
        return -1 # Not found


def transform(input_sequence):
    """
    Applies the transformation rule: finds the first '2', then searches after it
    for the first '0' followed by a non-zero digit. If found, removes that '0'
    and appends a '0' to the end. Otherwise, returns the sequence unchanged.

    Args:
        input_sequence: A numpy array of integers.

    Returns:
        A numpy array representing the potentially transformed sequence.
    """
    # Work with a Python list for easier manipulation (pop, append)
    # Keep the original input untouched unless modification is needed
    working_list = list(input_sequence)
    original_length = len(working_list)

    # 1. Find the index of the first occurrence of the integer 2
    first_two_index = find_first_occurrence(working_list, 2)

    # 2. If 2 is not found, return the original sequence unchanged.
    if first_two_index == -1:
        return input_sequence # Return original NumPy array

    # 3. Define the start index for searching after the first '2'
    search_start_index = first_two_index + 1
    target_zero_index = -1 # Initialize index for the '0' to remove

    # 4. Iterate through the list starting from index search_start_index
    #    up to the second-to-last element (index original_length - 2).
    #    The loop needs to check element `j` and `j+1`, so it stops at `len - 2`.
    for j in range(search_start_index, original_length - 1):
        # 5a. Check if the element list[j] is 0.
        # 5b. Check if the next element list[j + 1] is not 0.
        if working_list[j] == 0 and working_list[j + 1] != 0:
            # 5c. If both conditions are true, this is the target 0. Store index j and stop.
            target_zero_index = j
            break

    # 6. If a target 0 was found at index j:
    if target_zero_index != -1:
        # a. We already have a mutable copy (working_list).
        # b. Remove the element at index target_zero_index from the copy.
        working_list.pop(target_zero_index)
        # c. Append the integer 0 to the end of the copy.
        working_list.append(0)
        # d. Return the modified list as a numpy array.
        return np.array(working_list, dtype=input_sequence.dtype) # Match original dtype
    else:
        # 7. If the iteration completes without finding the target 0,
        #    return the original sequence unchanged.
        return input_sequence # Return original NumPy array