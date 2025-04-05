import numpy as np
import math

"""
Rearranges a sequence of 12 digits by swapping the first 8 digits with the last 4 digits.
The input is provided as a space-separated string of digits.
The output should also be a space-separated string of digits.
"""

def transform(input_str: str) -> str:
    """
    Transforms the input sequence by swapping the first 8 elements with the last 4.

    Args:
        input_str: A string containing 12 space-separated digits.

    Returns:
        A string containing the transformed sequence of 12 space-separated digits.
    """
    # Parse the input string into a list of strings (digits)
    input_list = input_str.split(' ')

    # Ensure the input has the expected length
    if len(input_list) != 12:
        raise ValueError("Input string must contain exactly 12 space-separated digits.")

    # Identify the first segment (first 8 elements)
    segment_1 = input_list[:8]

    # Identify the second segment (last 4 elements)
    segment_2 = input_list[8:]

    # Construct the output list by concatenating segment_2 followed by segment_1
    output_list = segment_2 + segment_1

    # Format the output list back into a space-separated string
    output_str = ' '.join(output_list)

    return output_str
