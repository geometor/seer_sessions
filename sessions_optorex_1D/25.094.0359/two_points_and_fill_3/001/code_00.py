import math
import numpy as np
import collections

"""
Identify the non-zero digit present in the input sequence. Let this digit be `d`.
Find the index (position) of the first occurrence of `d` in the input sequence (start_index).
Find the index (position) of the last occurrence of `d` in the input sequence (end_index).
Create the output sequence by copying the input sequence.
Iterate through the sequence positions from start_index to end_index (inclusive).
For each position in this range, set the digit in the output sequence to `d`.
The resulting sequence is the final output, formatted as a space-separated string.
"""

def find_non_zero_digit(int_list):
  """Finds the first non-zero digit in a list."""
  for digit in int_list:
    if digit != 0:
      return digit
  return None # Should not happen based on problem description

def find_first_last_indices(int_list, target_digit):
  """Finds the first and last indices of a target digit in a list."""
  first_index = -1
  last_index = -1
  for i, digit in enumerate(int_list):
    if digit == target_digit:
      if first_index == -1:
        first_index = i
      last_index = i
  return first_index, last_index

def transform(input_str: str) -> str:
    """
    Transforms the input string by filling the segment between the first and last
    occurrences of the non-zero digit with that digit.
    """
    # Parse the input string into a list of integers
    input_list = [int(d) for d in input_str.split()]

    # Initialize the output list as a copy of the input
    output_list = list(input_list)

    # 1. Identify the non-zero digit present in the input sequence.
    marker_digit = find_non_zero_digit(input_list)

    # Ensure a marker digit was found (as per problem constraints)
    if marker_digit is None:
        # Return the original input if no non-zero digit is found (edge case)
        return input_str 

    # 2. & 3. Find the first and last indices of the marker digit.
    start_index, end_index = find_first_last_indices(input_list, marker_digit)

    # Check if indices were found (should always be true based on problem description)
    if start_index == -1:
         # Return the original input if indices weren't found (edge case)
        return input_str

    # 4. Output is already initialized as a copy.
    # 5. & 6. Iterate from start_index to end_index and fill with marker_digit.
    for i in range(start_index, end_index + 1):
        output_list[i] = marker_digit

    # 7. Convert the output list back to a space-separated string.
    output_str = " ".join(map(str, output_list))

    return output_str
