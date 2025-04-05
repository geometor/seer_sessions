import math  # Not strictly needed for this version, but good practice if math ops were complex
from typing import List

"""
Transforms an input sequence (list) of 12 digits by cyclically shifting the 
subsequence of non-zero elements. The amount of the shift is determined by the 
count (N) of these non-zero elements according to a specific set of rules:
- N in {1, 2, 3, 4}: shift = 8
- N = 5: shift = 4
- N = 7: shift = 5
- N = 8: shift = 2
The shifted non-zero sequence is then placed back into a list of 12 zeros, 
starting at an index calculated by (original_first_non_zero_index + shift_amount) % 12,
wrapping around cyclically.
"""

def _get_shift_amount(n: int) -> int:
    """
    Determines the shift amount based on the count of non-zero elements (n).
    Uses the rules observed in the training data.
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
        # Based on the problem description, this might not occur,
        # but it's safer to handle it. A shift of 0 preserves position.
        # print(f"Warning: Unhandled count of non-zero elements: {n}. Defaulting shift to 0.")
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

    # Create a list containing only the non-zero integers, preserving order.
    non_zero_sequence = [x for x in input_list if x != 0]

    # Find the index of the first non-zero element in the original input list.
    first_nz_idx_in = -1
    for i, x in enumerate(input_list):
        if x != 0:
            first_nz_idx_in = i
            break

    # Handle the edge case: if the input list contains only zeros.
    if first_nz_idx_in == -1:
        return [0] * sequence_length # Return a list of all zeros

    # Count the number of non-zero elements.
    n = len(non_zero_sequence)

    # Determine the shift amount based on the count 'n'.
    shift_amount = _get_shift_amount(n)

    # Calculate the starting index for placing the non_zero_sequence in the output.
    # The modulo operator handles the cyclic nature.
    output_start_idx = (first_nz_idx_in + shift_amount) % sequence_length

    # Initialize the output list with zeros.
    output_list = [0] * sequence_length

    # Place the non_zero_sequence into the output list starting at output_start_idx,
    # wrapping around cyclically using the modulo operator.
    for i, value in enumerate(non_zero_sequence):
        output_index = (output_start_idx + i) % sequence_length
        output_list[output_index] = value

    # Return the fully constructed output list.
    return output_list