"""
Transforms an input sequence (list of integers) based on the following rule:
1. Creates a modifiable copy of the input sequence.
2. Identifies the target number, N, which is the value of the first element (at index 0) in the input sequence.
3. Searches the input sequence, starting from the fourth element (index 3), to find the index 'i' of the *first* occurrence of the target number N.
4. If such an index 'i' is found:
    a. Modifies the *copy* of the sequence: sets the value at index i-1 to N.
    b. Modifies the *copy* of the sequence: sets the value at index i to N.
    c. Modifies the *copy* of the sequence: sets the value at index i+1 to N.
5. Returns the modified copy as the output sequence. If N is not found after index 2, the original sequence copy is returned.
"""

import numpy as np
from typing import List

# Helper function to find the first occurrence of a value after a specific index
def find_first_occurrence_after_index(sequence: List[int], value: int, start_index: int) -> int:
    """
    Finds the index of the first occurrence of 'value' in 'sequence' at or after 'start_index'.

    Args:
        sequence: The list of integers to search within.
        value: The integer value to search for.
        start_index: The index from which to start searching (inclusive).

    Returns:
        The index of the first occurrence, or -1 if not found.
    """
    for i in range(start_index, len(sequence)):
        if sequence[i] == value:
            return i
    return -1 # Not found

def transform(input_list: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input list.
    """
    # Ensure input is a standard Python list for easier manipulation,
    # handling potential NumPy array input.
    if isinstance(input_list, np.ndarray):
        input_list = input_list.tolist()

    # 1. Create a modifiable copy of the input sequence.
    output_list = list(input_list)

    # Check if the list is long enough to perform the search (index 3)
    # and modification (index i-1, i+1). Requires len >= 4 for search,
    # and potentially more depending on where i is found.
    # Minimum length observed is 12, so >= 4 check is sufficient.
    if len(input_list) < 4:
        return output_list # Cannot perform the operation, return the copy

    # 2. Identify the target number N from the first element.
    n = input_list[0]

    # 3. Search for the first occurrence of N starting from index 3.
    start_search_index = 3
    found_index = find_first_occurrence_after_index(input_list, n, start_search_index)

    # 4. If N is found at index 'i'
    if found_index != -1:
        # Check if the surrounding indices i-1 and i+1 are valid.
        # Since search starts at index 3, found_index >= 3.
        # Thus, found_index - 1 >= 2, which is always a valid index.
        # We only need to check if found_index + 1 is within bounds.
        if found_index + 1 < len(output_list):
            # 4a. Modify the *copy* at index i-1
            output_list[found_index - 1] = n
            # 4b. Modify the *copy* at index i (already N, but set explicitly for clarity)
            output_list[found_index] = n
            # 4c. Modify the *copy* at index i+1
            output_list[found_index + 1] = n
        # else:
            # Handle edge case where N is found at the second-to-last position.
            # Based on examples, this doesn't seem to occur. If it did,
            # the rule might only apply to i-1 and i. However, sticking
            # to the observed pattern where i+1 is always valid.
            pass


    # 5. Return the modified copy.
    return output_list