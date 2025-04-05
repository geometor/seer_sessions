"""
Transforms an input sequence of 12 space-separated digits by performing a circular left shift of 8 positions.
"""

import collections

def circular_left_shift(data, shift):
    """
    Performs a circular left shift on a list.

    Args:
        data (list): The list to shift.
        shift (int): The number of positions to shift left.

    Returns:
        list: The shifted list.
    """
    if not data:
        return []
    n = len(data)
    shift = shift % n  # Ensure shift is within the bounds of the list length
    # Using collections.deque for efficient rotation
    d = collections.deque(data)
    d.rotate(-shift) # Negative rotation for left shift
    return list(d)
    # Alternative using slicing:
    # return data[shift:] + data[:shift]


def transform(input_string: str) -> str:
    """
    Applies a circular left shift of 8 positions to a sequence of 12 digits.

    Args:
        input_string: A string containing 12 space-separated digits.

    Returns:
        A string representing the transformed sequence, with digits space-separated.
    """
    # 1. Parse the input string into a sequence (list) of digits.
    # Split the string by spaces and convert each part to an integer.
    input_sequence = [int(x) for x in input_string.split()]

    # 2. Perform a circular left shift on the sequence by 8 positions.
    # Use the helper function for the shift.
    shifted_sequence = circular_left_shift(input_sequence, 8)

    # 3. Format the resulting sequence back into a space-separated string of digits.
    # Convert each integer back to a string and join them with spaces.
    output_string = " ".join(map(str, shifted_sequence))

    # 4. Return the formatted string.
    return output_string
