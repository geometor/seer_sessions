"""
Takes an input sequence of integers represented as a space-separated string,
sorts the integers in descending order, and returns the sorted sequence
as a space-separated string.
"""

import numpy as np # Although numpy isn't strictly needed for this specific task,
                  # it's often available and can handle array/list operations.
                  # Standard Python lists and sorting are sufficient here.

def transform(input_sequence_str: str) -> str:
    """
    Sorts a sequence of integers represented as a space-separated string in descending order.

    Args:
        input_sequence_str: A string containing space-separated integers.

    Returns:
        A string containing the sorted integers, space-separated.
    """
    # 1. Parse the input string into a list of integers.
    # Split the string by spaces and convert each part to an integer.
    input_list = [int(x) for x in input_sequence_str.split()]

    # 2. Sort the list of integers in descending order.
    # The reverse=True argument ensures sorting from largest to smallest.
    sorted_list = sorted(input_list, reverse=True)

    # 3. Format the sorted list back into a space-separated string.
    # Convert each integer back to a string and join them with spaces.
    output_sequence_str = " ".join(map(str, sorted_list))

    # 4. Return the resulting string.
    return output_sequence_str
