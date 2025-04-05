"""
Transforms an input sequence (list) of 12 digits by cyclically shifting the 
subsequence of non-zero elements. The amount of the shift is determined by the 
count (N) of these non-zero elements according to a specific set of rules:
- N in {1, 2, 3, 4}: shift = 8
- N = 5: shift = 4
- N = 7: shift = 5
- N = 8: shift = 2
- Otherwise: shift = 0 (default)
The shifted non-zero sequence is then placed back into a list of 12 zeros, 
starting at an index calculated by (original_first_non_zero_index + shift_amount) % 12,
wrapping around cyclically.
"""

from typing import List
import math # Not strictly required by current logic, but potentially useful for similar tasks

def _get_shift_amount(n: int) -> int:
    """
    Determines the shift amount based on the count of non-zero elements (n).
    Uses the rules observed in the training data.
    Args:
        n: The count of non-zero elements.
    Returns:
        The integer shift amount.
    """
    if n in [1, 2, 3, 4]:
        return 8
    elif n == 5:
        return 4
    elif n == 7:
        return 5
    elif n == 8:
        return 2
    else:
        # Default shift if N is outside the observed range.
        # A shift of 0 preserves position relative to the first non-zero index.
        return 0

def transform(input_list: List[int]) -> List[int]:
    """
    Applies the cyclic shift transformation to the input sequence list.

    Args:
        input_list: A list of 12 integers.

    Returns:
        A new list of 12 integers representing the transformed sequence.
    """
    sequence_length = 12 # Fixed length from observations

    # Step 1 & 2: Initialize and extract non-zeros and find the first index
    non_zero_sequence = []
    first_nz_idx_in = -1
    for i, x in enumerate(input_list):
        if x != 0:
            non_zero_sequence.append(x)
            if first_nz_idx_in == -1: # Record the index of the first non-zero element found
                first_nz_idx_in = i

    # Step 3: Count the number of non-zero elements (N)
    n = len(non_zero_sequence)

    # Step 4: Handle the edge case: if the input list contains only zeros
    if n == 0: # Equivalent to first_nz_idx_in == -1
        return [0] * sequence_length # Return a list of all zeros

    # Step 5: Determine the shift amount based on the count 'n' using the helper function
    shift_amount = _get_shift_amount(n)

    # Step 6: Calculate the starting index for placing the non_zero_sequence in the output list
    # The modulo operator handles the cyclic nature (wrapping around)
    output_start_idx = (first_nz_idx_in + shift_amount) % sequence_length

    # Step 7: Initialize the output list with zeros
    output_list = [0] * sequence_length

    # Step 8: Place the non_zero_sequence into the output list starting at output_start_idx,
    # wrapping around cyclically using the modulo operator for indices.
    for i, value in enumerate(non_zero_sequence):
        output_index = (output_start_idx + i) % sequence_length
        output_list[output_index] = value

    # Step 9: Return the fully constructed output list
    return output_list