import numpy as np

"""
Transforms an input sequence of 12 digits by performing a single left circular shift.
The first digit moves to the last position, and all other digits shift one position to the left.
"""

def transform(input_sequence_str: str) -> str:
    """
    Performs a left circular shift on a sequence of digits represented as a string.

    Args:
        input_sequence_str: A string representing the input sequence of digits, separated by spaces.

    Returns:
        A string representing the output sequence of digits after the shift, separated by spaces.
    """
    # Parse the input string into a list of integers
    input_list = [int(digit) for digit in input_sequence_str.split()]

    # Check if the list is empty to avoid index errors
    if not input_list:
        return "" # Return empty string or handle as appropriate

    # Store the first element
    first_element = input_list[0]

    # Create the shifted list by taking elements from the second position onwards
    shifted_list = input_list[1:]

    # Append the original first element to the end of the shifted list
    output_list = shifted_list + [first_element]

    # Format the output list back into a space-separated string
    output_sequence_str = " ".join(map(str, output_list))

    return output_sequence_str
