"""
Transforms an input sequence of 12 integers by moving the last 3 elements to the beginning.
This is equivalent to a right circular shift of the sequence by 3 positions.
"""

import re

def parse_input(input_str):
  """Parses the space-separated string into a list of integers."""
  return [int(x) for x in input_str.strip().split()]

def format_output(output_list):
  """Formats a list of integers into a space-separated string."""
  return " ".join(map(str, output_list))

def transform(input_str: str) -> str:
    """
    Performs a right circular shift by 3 positions on the input sequence.

    Args:
        input_str: A string containing 12 space-separated integers.

    Returns:
        A string containing the transformed sequence of 12 space-separated integers.
    """
    # Parse the input string into a list of integers
    input_list = parse_input(input_str)

    # Check if the input list has the expected length (optional but good practice)
    if len(input_list) != 12:
        # Handle error or unexpected input length if necessary
        # For this task, we assume valid input
        pass 

    # Identify the last three elements
    last_three = input_list[-3:]

    # Identify the first nine elements
    first_nine = input_list[:-3]

    # Construct the output list by concatenating the parts
    # The last three elements come first, followed by the first nine
    output_list = last_three + first_nine

    # Format the output list back into a space-separated string
    output_str = format_output(output_list)

    return output_str
