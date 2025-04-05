```python
import math
import numpy as np
from typing import List, Union

"""
Reverses the segment of the input sequence lying between the first non-zero digit 
and the last non-zero digit (inclusive), leaving any leading or trailing zeros 
in their original positions. If the sequence contains only zeros, it remains unchanged. 
The input and output are strings of space-separated digits.
"""

def _find_first_non_zero_index(digit_list: List[int]) -> int:
    """Finds the index of the first non-zero digit in the list."""
    for i, digit in enumerate(digit_list):
        if digit != 0:
            return i
    return -1 # Indicates all zeros

def _find_last_non_zero_index(digit_list: List[int]) -> int:
    """Finds the index of the last non-zero digit in the list."""
    # Iterate backwards to find the last non-zero element efficiently
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
    # Step 1 & 2: Parse the input string into a list of integers.
    input_list = [int(d) for d in input_str.split()]

    # Step 3: Find the index of the first non-zero integer.
    first_nz_idx = _find_first_non_zero_index(input_list)

    # Step 8: Handle the case where all digits are zero.
    if first_nz_idx == -1:
        return input_str # Return original string if all zeros

    # Step 4: Find the index of the last non-zero integer.
    # This is guaranteed to exist if first_nz_idx != -1.
    last_nz_idx = _find_last_non_zero_index(input_list)

    # Step 5: Identify and extract the three segments.
    # a. Leading Zeros
    leading_zeros = input_list[:first_nz_idx]
    # b. NonZeroSegment (the part to be reversed)
    segment_to_reverse = input_list[first_nz_idx : last_nz_idx + 1]
    # c. Trailing Zeros
    trailing_zeros = input_list[last_nz_idx + 1 :]

    # Step 6: Reverse the order of the integers within the NonZeroSegment.
    reversed_segment = segment_to_reverse[::-1] # Using list slicing for reversal

    # Step 7: Construct the output list by concatenating the parts.
    output_list = leading_zeros + reversed_segment + trailing_zeros

    # Step 9: Convert the resulting output list back into a space-separated string.
    output_str = " ".join(map(str, output_list))

    # Step 10: Return the final string.
    return output_str

```