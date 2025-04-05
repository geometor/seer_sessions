import collections

"""
Rearrange the input sequence of integers (0, 1, 2) such that all 2s appear first, 
followed by all 0s, and finally all 1s, maintaining the original counts of each integer.
"""

def transform(input_str: str) -> str:
    """
    Transforms an input string of space-separated integers (0, 1, 2)
    by rearranging them according to the custom sort order: 2, 0, 1.

    Args:
        input_str: A string containing space-separated integers (0, 1, or 2).

    Returns:
        A string containing the rearranged integers, space-separated.
    """
    # Parse the input string into a list of integers
    # Handle potential empty strings resulting from multiple spaces
    numbers = [int(x) for x in input_str.split() if x]

    # Count the occurrences of each number (0, 1, 2)
    counts = collections.Counter(numbers)
    count_0 = counts.get(0, 0)
    count_1 = counts.get(1, 0)
    count_2 = counts.get(2, 0)

    # Construct the output list based on the custom sort order (2, 0, 1)
    output_list = []
    # Append all the 2s
    output_list.extend([2] * count_2)
    # Append all the 0s
    output_list.extend([0] * count_0)
    # Append all the 1s
    output_list.extend([1] * count_1)

    # Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_list))

    return output_str
