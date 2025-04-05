import math
import numpy as np
import collections

"""
Perform a left rotation on a sequence of integers. The first element of the input sequence is moved to the last position, shifting all other elements one position to the left.
"""

def parse_input(input_str: str) -> list[int]:
    """Parses a space-separated string of integers into a list of integers."""
    return [int(x) for x in input_str.split()]

def format_output(output_list: list[int]) -> str:
    """Formats a list of integers into a space-separated string."""
    return " ".join(map(str, output_list))

def transform(input_str: str) -> str:
    """
    Transforms the input sequence by performing a left circular shift by one position.

    Args:
        input_str: A string containing space-separated integers representing the input sequence.

    Returns:
        A string containing space-separated integers representing the transformed sequence.
    """
    # Parse the input string into a list of integers
    input_list = parse_input(input_str)

    # Handle empty or single-element lists (rotation has no effect or is trivial)
    if len(input_list) <= 1:
        return input_str # Return the original string representation

    # Identify the first element
    first_element = input_list[0]

    # Create a new list containing all elements except the first one
    rest_of_list = input_list[1:]

    # Append the first element to the end of the new list
    output_list = rest_of_list + [first_element]

    # Format the resulting list back into a space-separated string
    output_str = format_output(output_list)

    return output_str
