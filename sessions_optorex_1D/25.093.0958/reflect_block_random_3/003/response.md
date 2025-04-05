```python
import math
import numpy as np
from typing import List, Union

"""
Reverses the segment of the input sequence lying between the first non-zero digit 
and the last non-zero digit (inclusive), leaving any leading or trailing zeros 
in their original positions. If the sequence contains only zeros, it remains unchanged.
The input is expected to be a sequence (list or NumPy array) of integers.
"""

def _find_first_non_zero_index(digit_list: Union[List[int], np.ndarray]) -> int:
    """Finds the index of the first non-zero digit in the sequence."""
    for i, digit in enumerate(digit_list):
        if digit != 0:
            return i
    return -1 # Indicates all zeros

def _find_last_non_zero_index(digit_list: Union[List[int], np.ndarray]) -> int:
    """Finds the index of the last non-zero digit in the sequence."""
    # Iterate backwards to find the last non-zero element efficiently
    for i in range(len(digit_list) - 1, -1, -1):
        if digit_list[i] != 0:
            return i
    return -1 # Indicates all zeros

def transform(input_sequence: Union[List[int], np.ndarray]) -> Union[List[int], np.ndarray]:
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A sequence (list or NumPy array) of 12 integers.

    Returns:
        A sequence of the same type as the input, representing the transformed sequence.
    """
    # Ensure working with a list for consistent slicing and concatenation
    # (NumPy arrays might require different handling for concatenation if not careful)
    # Although standard slicing and concatenation work similarly here.
    # We'll keep it general but prefer list operations internally.
    if isinstance(input_sequence, np.ndarray):
        input_list = input_sequence.tolist()
        is_numpy = True
    else:
        # Assume it's already list-like (e.g., a list)
        input_list = list(input_sequence)
        is_numpy = False

    # Find the index of the first non-zero digit
    first_nz_idx = _find_first_non_zero_index(input_list)

    # Handle the case where all digits are zero
    if first_nz_idx == -1:
        # If all zeros, return the original sequence in its original type
        return input_sequence

    # Find the index of the last non-zero digit (guaranteed to exist if first_nz_idx != -1)
    last_nz_idx = _find_last_non_zero_index(input_list)

    # Extract the leading zeros (if any)
    # Slice from beginning up to the first non-zero index
    leading_zeros = input_list[:first_nz_idx]

    # Extract the segment to be reversed
    # Slice from the first non-zero index up to and including the last non-zero index
    segment_to_reverse = input_list[first_nz_idx : last_nz_idx + 1]

    # Extract the trailing zeros (if any)
    # Slice from the index after the last non-zero index to the end
    trailing_zeros = input_list[last_nz_idx + 1 :]

    # Reverse the middle segment
    reversed_segment = segment_to_reverse[::-1] # Using list slicing for reversal

    # Reconstruct the list by concatenating the parts
    output_list = leading_zeros + reversed_segment + trailing_zeros

    # Convert back to NumPy array if the input was an array
    if is_numpy:
        return np.array(output_list, dtype=input_sequence.dtype) # Preserve original dtype if numpy
    else:
        return output_list
```