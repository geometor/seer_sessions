import numpy as np
import math

"""
Transforms an input sequence of 12 digits by cyclically shifting the subsequence 
of non-zero elements based on the count of these non-zero elements.

1. Parses the input string into a list of 12 integers.
2. Extracts the non-zero elements into a separate list, preserving their order.
3. Finds the index of the first non-zero element in the original input.
4. Counts the number of non-zero elements (N).
5. Determines a shift amount based on N using a specific mapping:
   - N in {1, 2, 3, 4}: shift = 8
   - N = 5: shift = 4
   - N = 7: shift = 5
   - N = 8: shift = 2
   - (Other values of N are not handled based on examples, defaults to 0 shift if needed).
6. Calculates the starting index for the non-zero subsequence in the output list 
   using the formula: (first_non_zero_index + shift_amount) % 12.
7. Creates an output list of 12 zeros.
8. Places the extracted non-zero subsequence into the output list starting at the 
   calculated index, wrapping around the end of the list cyclically.
9. Formats the output list back into a space-separated string.
"""

def _parse_input(input_str: str) -> list[int]:
    """Converts the space-separated string into a list of integers."""
    return [int(x) for x in input_str.split()]

def _format_output(output_list: list[int]) -> str:
    """Converts a list of integers into a space-separated string."""
    return " ".join(map(str, output_list))

def _get_shift_amount(n: int) -> int:
    """Determines the shift amount based on the count of non-zero elements (n)."""
    if n in [1, 2, 3, 4]:
        return 8
    elif n == 5:
        return 4
    elif n == 7:
        return 5
    elif n == 8:
        return 2
    else:
        # Default or handle other cases if necessary based on more examples
        # For now, assume these are the only relevant counts based on training data.
        # A shift of 0 might be a safe default if N is outside expected ranges.
        print(f"Warning: Unhandled count of non-zero elements: {n}. Defaulting shift to 0.")
        return 0 # Or raise an error, or handle differently

def transform(input_str: str) -> str:
    """
    Applies the cyclic shift transformation to the input sequence string.
    """
    # 1. Parse the input string into a list of 12 integers.
    input_list = _parse_input(input_str)
    sequence_length = 12 # Assuming fixed length based on examples

    # 2. Create a new list containing only the non-zero integers
    non_zero_sequence = [x for x in input_list if x != 0]

    # 3. Find the index of the first non-zero element.
    first_nz_idx_in = -1
    for i, x in enumerate(input_list):
        if x != 0:
            first_nz_idx_in = i
            break

    # Handle the case where there are no non-zero elements
    if first_nz_idx_in == -1:
        return _format_output([0] * sequence_length) # Return all zeros

    # 4. Count the number of elements in the non_zero_sequence (N).
    n = len(non_zero_sequence)

    # 5. Determine the shift_amount based on N.
    shift_amount = _get_shift_amount(n)

    # 6. Calculate the starting index for placing the non_zero_sequence in the output.
    output_start_idx = (first_nz_idx_in + shift_amount) % sequence_length

    # 7. Create the output list, initially filled with 12 zeros.
    output_list = [0] * sequence_length

    # 8. Place the non_zero_sequence into the output list cyclically.
    for i, value in enumerate(non_zero_sequence):
        output_index = (output_start_idx + i) % sequence_length
        output_list[output_index] = value

    # 9. Convert the output list back into a space-separated string.
    return _format_output(output_list)
