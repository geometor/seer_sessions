"""
Takes an input sequence of 12 integers (0, 1, or 2) and sorts them in descending order to produce the output sequence.
"""

import numpy as np

def transform(input_sequence_str: str) -> str:
    """
    Sorts a sequence of integers represented as a space-separated string in descending order.

    Args:
        input_sequence_str: A string containing space-separated integers (0, 1, or 2).

    Returns:
        A string containing the sorted integers, space-separated.
    """
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_sequence_str.split()]

    # Sort the list in descending order
    # The reverse=True argument sorts from largest to smallest
    output_list = sorted(input_list, reverse=True)

    # Format the output list back into a space-separated string
    output_sequence_str = " ".join(map(str, output_list))

    return output_sequence_str
