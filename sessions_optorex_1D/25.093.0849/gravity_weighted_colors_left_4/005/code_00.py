"""
Transforms an input sequence (list or array) of integers (0, 1, 2) by sorting the integers numerically in non-decreasing (ascending) order and returning the sorted sequence formatted as a space-separated string.
"""

import numpy as np # Import numpy as the input might be a numpy array

def transform(input_data) -> str:
    """
    Sorts the integers in an input sequence and formats them as a space-separated string.

    Args:
        input_data: A sequence (list or NumPy array) containing integers (0, 1, 2).

    Returns:
        A string containing the same integers as the input, sorted numerically
        in non-decreasing order and separated by spaces.
    """
    # 1. Sort the integers in the input sequence numerically in non-decreasing order.
    #    Using sorted() handles both lists and numpy arrays, returning a sorted list.
    #    Example: [0, 1, 0, 0, 2, 0, 0, 0, 2, 2, 0, 0] -> [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2]
    sorted_integers = sorted(input_data)

    # 2. Convert each integer in the sorted sequence into its string representation.
    #    Example: [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2] -> ['0', '0', '0', '0', '0', '0', '0', '0', '1', '2', '2', '2']
    sorted_strings = [str(num) for num in sorted_integers]

    # 3. Join these string representations together into a single string,
    #    using a single space character as the separator.
    #    Example: ['0', '0', '0', '0', '0', '0', '0', '0', '1', '2', '2', '2'] -> "0 0 0 0 0 0 0 0 1 2 2 2"
    output_str = ' '.join(sorted_strings)

    # 4. Return the resulting space-separated string.
    return output_str