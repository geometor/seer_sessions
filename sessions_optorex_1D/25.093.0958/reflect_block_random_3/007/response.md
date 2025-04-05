```python
import numpy as np
from typing import List, Union

"""
Reverses the segment of an input sequence of 12 integers lying between the 
first non-zero integer and the last non-zero integer (inclusive), leaving any 
leading or trailing zeros in their original positions. If the sequence contains 
only zeros, it remains unchanged. The input and output are sequences of the 
same type (either List[int] or numpy.ndarray).
"""

def _find_first_non_zero_index(sequence: Union[List[int], np.ndarray]) -> int:
    """Finds the index of the first non-zero integer in the sequence."""
    # Iterate through the sequence with index
    for i, element in enumerate(sequence):
        # Check if the element is not zero
        if element != 0:
            # Return the index of the first non-zero element
            return i
    # If no non-zero element is found after checking all elements
    return -1 # Indicate that all elements are zero

def _find_last_non_zero_index(sequence: Union[List[int], np.ndarray]) -> int:
    """Finds the index of the last non-zero integer in the sequence."""
    # Iterate backwards through the sequence with index
    for i in range(len(sequence) - 1, -1, -1):
        # Check if the element at the current index is not zero
        if sequence[i] != 0:
            # Return the index of the last non-zero element
            return i
    # If no non-zero element is found (this case should technically be caught
    # by the first_non_zero check in the main function, but included for completeness)
    return -1 # Indicate that all elements are zero


def transform(input_sequence: Union[List[int], np.ndarray]) -> Union[List[int], np.ndarray]:
    """
    Applies the reversal transformation to the relevant segment of the input sequence.

    Args:
        input_sequence: A sequence (list or NumPy array) of 12 integers.

    Returns:
        A sequence of the same type as the input, representing the transformed sequence.
    """

    # Step 1: Check the input type to return the same type later.
    # Using isinstance() to check if the input is a NumPy array.
    is_numpy = isinstance(input_sequence, np.ndarray)
    # Convert to list for consistent slicing/reversal operations, regardless of input type.
    # This simplifies handling compared to managing both list and numpy array operations separately.
    if is_numpy:
        working_list = input_sequence.tolist()
    else:
        # Ensure it's a mutable list if it's not a NumPy array (e.g., could be a tuple)
        working_list = list(input_sequence)

    # Step 2: Find the index of the first non-zero integer.
    first_nz_idx = _find_first_non_zero_index(working_list)

    # Step 3: Handle the all-zeros case.
    # If first_nz_idx is -1, it means all elements were zero.
    if first_nz_idx == -1:
        # Return the original input sequence without modification.
        return input_sequence

    # Step 4: Find the index of the last non-zero integer.
    # This is only needed if there is at least one non-zero element.
    last_nz_idx = _find_last_non_zero_index(working_list)

    # Step 5: Extract the leading zeros segment.
    # Slice from the beginning up to (but not including) the first non-zero index.
    leading_zeros = working_list[:first_nz_idx]

    # Step 6: Extract the non-zero segment to be reversed.
    # Slice from the first non-zero index up to and including the last non-zero index.
    segment_to_reverse = working_list[first_nz_idx : last_nz_idx + 1]

    # Step 7: Extract the trailing zeros segment.
    # Slice from the index immediately after the last non-zero index to the end.
    trailing_zeros = working_list[last_nz_idx + 1 :]

    # Step 8: Reverse the non-zero segment.
    # Use slicing with step -1 to create a reversed copy of the segment.
    reversed_segment = segment_to_reverse[::-1]

    # Step 9: Construct the final output list by concatenating the parts.
    # Combine the leading zeros, the reversed middle segment, and the trailing zeros.
    output_list = leading_zeros + reversed_segment + trailing_zeros

    # Step 10: Ensure the output is the same type as the input.
    # If the original input was a NumPy array, convert the result list back to a NumPy array.
    if is_numpy:
        # Preserve the original data type if it was a NumPy array.
        return np.array(output_list, dtype=input_sequence.dtype)
    else:
        # Otherwise, return the result as a list.
        return output_list

```