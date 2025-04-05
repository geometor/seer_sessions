import math
import collections

"""
Parses an input string of space-separated integers, sorts these integers in ascending numerical order, 
and formats the sorted sequence back into a space-separated string.
"""

def parse_input(input_str):
  """Converts a space-separated string of numbers into a list of integers."""
  return [int(x) for x in input_str.split()]

def format_output(int_list):
  """Converts a list of integers into a space-separated string."""
  return " ".join(map(str, int_list))

def transform(input_str: str) -> str:
    """
    Transforms an input string of space-separated integers by sorting them
    in ascending order.

    Args:
        input_str: A string containing space-separated integers.

    Returns:
        A string containing the sorted integers, separated by spaces.
    """
    # 1. Parse the input string into a list of integers.
    int_list = parse_input(input_str)

    # 2. Sort the list of integers in non-decreasing (ascending) numerical order.
    # Using sorted() creates a new sorted list without modifying the original
    sorted_list = sorted(int_list)

    # 3. Format the sorted list of integers back into a space-separated string.
    output_str = format_output(sorted_list)

    # 4. Return the formatted string as the output.
    return output_str
