import collections

"""
Sorts the input sequence of integers in descending order.
"""

def transform(input_str):
    """
    Takes a space-separated string of integers, sorts them in descending order,
    and returns the sorted sequence as a space-separated string.

    Args:
        input_str: A string containing space-separated integers (0, 1, or 2).

    Returns:
        A string containing the sorted integers, space-separated.
    """
    # Parse the input string into a list of integers
    # Example: "1 2 0" -> [1, 2, 0]
    input_list = [int(x) for x in input_str.split()]

    # Sort the list of integers in descending order
    # Example: [1, 2, 0] -> [2, 1, 0]
    sorted_list = sorted(input_list, reverse=True)

    # Format the sorted list back into a space-separated string
    # Example: [2, 1, 0] -> "2 1 0"
    output_str = " ".join(map(str, sorted_list))

    return output_str
