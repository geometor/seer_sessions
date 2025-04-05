```python
import math
import numpy as np

"""
Reverses the segment of the input sequence lying between the first non-zero digit 
and the last non-zero digit (inclusive), leaving any leading or trailing zeros 
in their original positions. If the sequence contains only zeros, it remains unchanged.
"""

def _find_first_non_zero_index(digit_list):
    """Finds the index of the first non-zero digit."""
    for i, digit in enumerate(digit_list):
        if digit != 0:
            return i
    return -1 # Indicates all zeros

def _find_last_non_zero_index(digit_list):
    """Finds the index of the last non-zero digit."""
    for i in range(len(digit_list) - 1, -1, -1):
        if digit_list[i] != 0:
            return i
    return -1 # Indicates all zeros

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string.

    Args:
        input_str: A string of space-separated single digits (e.g., "0 6 3 1 1 9 1 6 1 2 9 4").

    Returns:
        A string representing the transformed sequence of digits, space-separated.
    """
    # Parse the input string into a list of integers
    input_list = [int(d) for d in input_str.split()]

    # Find the index of the first non-zero digit
    first_nz_idx = _find_first_non_zero_index(input_list)

    # Handle the case where all digits are zero
    if first_nz_idx == -1:
        return input_str # Return original string if all zeros

    # Find the index of the last non-zero digit
    last_nz_idx = _find_last_non_zero_index(input_list)

    # Extract the leading zeros (if any)
    leading_zeros = input_list[:first_nz_idx]

    # Extract the segment to be reversed
    segment_to_reverse = input_list[first_nz_idx:last_nz_idx+1]

    # Extract the trailing zeros (if any)
    trailing_zeros = input_list[last_nz_idx+1:]

    # Reverse the middle segment
    reversed_segment = segment_to_reverse[::-1] # Using slicing for reversal

    # Reconstruct the list by combining the parts
    output_list = leading_zeros + reversed_segment + trailing_zeros

    # Format the output list back into a space-separated string
    output_str = " ".join(map(str, output_list))

    return output_str

```