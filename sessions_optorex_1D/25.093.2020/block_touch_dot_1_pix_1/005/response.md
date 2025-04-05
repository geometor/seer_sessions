```python
import numpy as np
import math

"""
Find the index `i` of the *first* occurrence of the digit `2` in the sequence.
If `2` is not found, return the original input sequence unchanged.
If `2` is found at index `i`, proceed to search the subsequence starting from index `i + 1` up to the second-to-last element of the original sequence.
Iterate through this subsequence, checking each element at index `j` (where `j` ranges from `i + 1` to `length - 2`):
  a. Check if the element `sequence[j]` is equal to `0`.
  b. Check if the *next* element `sequence[j + 1]` is *not* equal to `0`.
  c. If both conditions (a and b) are met, this `0` at index `j` is the target. Record this index `j` as `target_index` and immediately stop this search iteration.
After completing the search:
  a. If a `target_index` was recorded:
     i. Create a new sequence by removing the element at `target_index` from the original sequence.
     ii. Append a `0` to the end of this new sequence.
     iii. Return the modified sequence.
  b. If no `target_index` was recorded: Return the original input sequence unchanged.
"""

def find_first_occurrence(sequence_list, value):
    """
    Helper function to find the index of the first occurrence of a value in a list.
    Returns -1 if the value is not found.
    """
    try:
        return sequence_list.index(value)
    except ValueError:
        return -1

def transform(input_sequence: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input sequence (numpy array).
    """
    # Convert numpy array to list for easier manipulation (index, pop, append)
    working_list = list(input_sequence)
    original_length = len(working_list)

    # 1. Find the index i of the first occurrence of the digit 2
    first_two_index = find_first_occurrence(working_list, 2)

    # 2. If 2 is not found, return the original sequence unchanged.
    if first_two_index == -1:
        return input_sequence # Return original NumPy array

    # 3. Define the start index for searching after the first '2'
    search_start_index = first_two_index + 1
    target_zero_index = -1 # Initialize index for the '0' to remove

    # 4. Iterate through the subsequence from index i + 1 up to length - 2
    #    The loop needs to check element `j` and `j+1`, so it stops before the last element.
    for j in range(search_start_index, original_length - 1):
        # 5a. Check if the element list[j] is 0.
        # 5b. Check if the next element list[j + 1] is not 0.
        if working_list[j] == 0 and working_list[j + 1] != 0:
            # 5c. If both conditions true, record target index j and stop searching.
            target_zero_index = j
            break # Found the first match, stop the loop

    # 6. After completing the search:
    # 6a. If a target_index was recorded (meaning the condition was met):
    if target_zero_index != -1:
        # i. Create a new sequence by removing the element at target_index.
        #    (working_list is already a mutable copy)
        working_list.pop(target_zero_index)
        # ii. Append a 0 to the end of this new sequence.
        working_list.append(0)
        # iii. Return the modified sequence as a numpy array, preserving original dtype.
        return np.array(working_list, dtype=input_sequence.dtype)
    else:
        # 6b. If no target_index was recorded (condition never met):
        #     Return the original input sequence unchanged.
        return input_sequence # Return original NumPy array
```