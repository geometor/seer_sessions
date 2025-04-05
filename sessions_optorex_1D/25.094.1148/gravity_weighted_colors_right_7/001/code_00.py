import collections

"""
Accept the input sequence of digits, sort the digits within the sequence in descending order (from 2 down to 0), and return the sorted sequence.
"""

def transform(input_str):
    """
    Sorts a sequence of digits (represented as a space-separated string)
    in descending order.

    Args:
        input_str: A string containing space-separated digits (0, 1, or 2).

    Returns:
        A list of integers sorted in descending order.
    """
    # Convert the input string into a list of integers
    # Example: "2 1 0 0 0 0 0 0 2 0 1 2" -> [2, 1, 0, 0, 0, 0, 0, 0, 2, 0, 1, 2]
    input_list = [int(digit) for digit in input_str.split()]

    # Sort the list of digits in descending order
    # Example: [2, 1, 0, 0, 0, 0, 0, 0, 2, 0, 1, 2] -> [2, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0]
    output_list = sorted(input_list, reverse=True)

    # Return the sorted list
    return output_list
