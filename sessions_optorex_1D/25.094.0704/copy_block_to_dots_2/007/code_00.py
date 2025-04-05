import numpy as np
import math
import collections # Although not strictly needed for this version, keeping it as it might be useful for future refinements.

"""
Transforms an input sequence (provided as a NumPy array of 12 integers) based on a specific rule.
The rule identifies 'trigger points' where a non-zero integer N appears at index i (where 3 <= i < length-1)
and is preceded by a different integer (usually 0). For each trigger point i found
in the *original* input sequence, the elements at indices i-1, i, and i+1 in a *copy* of the
sequence are replaced with N.

The function takes a NumPy array as input and returns a standard Python list representing the transformed sequence.
"""

def _find_first_non_zero(sequence: list[int]) -> int | None:
    """
    Finds the first non-zero value in the sequence.
    Helper function to identify the characteristic non-zero integer 'N'.
    Returns None if the sequence contains only zeros.
    """
    for val in sequence:
        if val != 0:
            return val
    return None # Return None if all are zero

def _find_trigger_indices(sequence: list[int], non_zero_val: int) -> list[int]:
    """
    Finds indices 'i' that meet the trigger conditions:
    1. 3 <= i < len(sequence) - 1  (ensures i-1 and i+1 are valid for access/replacement)
    2. sequence[i] == non_zero_val
    3. sequence[i-1] != non_zero_val
    Helper function to locate all points in the original sequence that initiate the transformation.
    """
    trigger_indices = []
    list_len = len(sequence)
    # The loop must start at 3 and end at list_len - 2 (exclusive end) to ensure
    # sequence[i-1] (index >= 2) and sequence[i+1] (index <= list_len - 1) are valid.
    # Minimum length required for any trigger is 4 (for i=3 to exist with i+1=4).
    if list_len < 4:
        return [] # No possible triggers if list is shorter than 4 elements

    # Iterate through the possible range for 'i'
    for i in range(3, list_len - 1):
        # Check the trigger conditions
        if sequence[i] == non_zero_val and sequence[i-1] != non_zero_val:
            trigger_indices.append(i) # Store the index if conditions are met
            
    return trigger_indices

def transform(input_array: np.ndarray) -> list[int]:
    """
    Applies the transformation rule to the input NumPy array.
    """
    # 1. Convert NumPy array to Python list for easier index-based manipulation.
    input_list = input_array.tolist()
    list_len = len(input_list)

    # 2. Identify the primary non-zero integer N using the helper function.
    non_zero_val = _find_first_non_zero(input_list)

    # 3. Handle edge cases: If all elements are zero or the list is too short
    #    for any trigger (length < 4), no transformation is possible. Return the original list.
    if non_zero_val is None or list_len < 4:
        return input_list

    # 4. Create an independent, modifiable copy of the input sequence. This is crucial
    #    as modifications should not affect subsequent trigger identification based on the original input.
    output_list = list(input_list)

    # 5. Find all trigger indices 'i' in the *original* input list using the helper function.
    trigger_indices = _find_trigger_indices(input_list, non_zero_val)

    # 6. Iterate through each identified trigger index.
    for i in trigger_indices:
        # For each trigger index 'i', modify the 'output_list' (the copy)
        # at indices i-1, i, and i+1, setting them to N (non_zero_val).
        # The bounds for these indices are guaranteed to be valid because
        # _find_trigger_indices only returns 'i' where 3 <= i < list_len - 1.
        output_list[i-1] = non_zero_val
        output_list[i]   = non_zero_val
        output_list[i+1] = non_zero_val

    # 7. Return the final modified list.
    return output_list