```python
import numpy as np

"""
Examine the input sequence of integers to find the index `i` of the *first* occurrence of the digit `2`.
If the digit `2` is *not present* in the sequence, return the original input sequence without any changes.
If the digit `2` is found at index `i`, initiate a search within the sequence. This search starts at the index *immediately following* `i` (i.e., index `i + 1`) and continues up to, but *does not include*, the last element of the sequence (i.e., up to index `length - 2`).
During the search, for each element at the current index `j`:
  a.  Check if the element `sequence[j]` is equal to `0`.
  b.  Check if the *next* element in the sequence, `sequence[j + 1]`, is *not* equal to `0`.
If *both* conditions (a and b) are true for an element at index `j`, then this is the *target element* for transformation. Record this index `j` as the `target_index` and immediately *stop* the search process (only the first such occurrence matters).
After completing the search (either by finding a target or reaching the end of the search range):
  a.  If a `target_index` *was* recorded: Create a new sequence by taking the original sequence, removing the element at the `target_index`, and then appending a single `0` to the very end. Return this newly constructed sequence.
  b.  If *no* `target_index` was recorded (because the condition in step 5 was never met within the search range), return the original input sequence without any changes.
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
    Applies the transformation rule to the input numpy array sequence.
    """
    # Convert numpy array to a Python list for easier index finding and manipulation
    working_list = list(input_sequence)
    original_length = len(working_list)

    # 1. Find the index i of the first occurrence of the digit 2
    first_two_index = find_first_occurrence(working_list, 2)

    # 2. If 2 is not found, return the original sequence unchanged.
    if first_two_index == -1:
        return input_sequence # Return original NumPy array

    # 3. Define the start index for searching after the first '2'
    #    The search range goes up to index original_length - 2 because we need to check index j+1
    search_start_index = first_two_index + 1
    target_index = -1 # Initialize index for the '0' to remove

    # 4. & 5. Iterate through the sequence starting from after the first '2',
    #          looking for the first '0' followed by a non-'0'.
    for j in range(search_start_index, original_length - 1):
        # 5a. Check if the element list[j] is 0.
        # 5b. Check if the next element list[j + 1] is not 0.
        if working_list[j] == 0 and working_list[j + 1] != 0:
            # 5c. If both conditions true, record target index j and stop searching.
            target_index = j
            break # Found the first match, stop the loop

    # 6. After completing the search:
    # 6a. If a target_index was recorded:
    if target_index != -1:
        # i. Remove the element at target_index from the working list.
        working_list.pop(target_index)
        # ii. Append a 0 to the end of this modified list.
        working_list.append(0)
        # iii. Return the modified sequence as a numpy array, preserving original dtype.
        return np.array(working_list, dtype=input_sequence.dtype)
    # 6b. If no target_index was recorded:
    else:
        # Return the original input sequence unchanged.
        return input_sequence
```