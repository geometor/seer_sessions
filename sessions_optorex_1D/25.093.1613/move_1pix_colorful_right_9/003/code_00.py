"""
Parses an input string containing 12 space-separated integers into a list of integers.
Then, transforms this list by taking the first 11 elements and prepending a 0 to create the output list of 12 integers.
"""

import numpy as np # Using numpy arrays can be efficient for slicing, though lists work fine too.

def parse_input_string(input_str: str) -> list[int]:
  """
  Parses a string of space-separated integers into a list of integers.

  Args:
    input_str: The input string containing space-separated integers.

  Returns:
    A list of integers derived from the input string.
  """
  try:
    # Split the string by spaces and convert each part to an integer
    parsed_list = [int(x) for x in input_str.split()]
    # Basic validation for expected length after parsing
    if len(parsed_list) != 12:
        # This case might indicate unexpected input format if it occurs
        print(f"Warning: Parsed list length is {len(parsed_list)}, expected 12. Input: '{input_str}'")
    return parsed_list
  except ValueError:
    # Handle cases where conversion to int fails
    raise ValueError(f"Input string contains non-integer values: '{input_str}'")


def transform(input_str: str) -> list[int]:
  """
  Transforms the input string sequence according to the observed rule.

  Args:
    input_str: A string containing 12 space-separated integers.

  Returns:
    A list of 12 integers representing the transformed sequence.
  """

  # 1. Parse the input string into a list of integers
  input_list = parse_input_string(input_str)

  # 2. Create a new list by taking the first 11 integers from the parsed list
  #    (This effectively discards the last element)
  truncated_list = input_list[:-1]

  # 3. Insert the integer 0 at the beginning of this new list
  output_list = [0] + truncated_list

  # 4. Return the resulting 12-integer list
  return output_list
