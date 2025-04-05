import math # Not strictly necessary for this task, but included per template habit
import numpy as np # Not strictly necessary, input is string, but useful for potential future variations
from typing import List

"""
Transforms a space-separated string of integers into a space-separated binary string (0s and 1s).
The output string has the same number of elements as the input string.
The number of leading '1's in the output string equals the count of non-zero integers in the input string.
The remaining elements in the output string are '0's.
"""

def parse_input_string(input_str: str) -> List[int]:
    """Parses a space-separated string into a list of integers."""
    if not input_str: # Handle empty input string case
        return []
    return [int(s) for s in input_str.split()]

def count_non_zeros(int_list: List[int]) -> int:
  """Counts the number of non-zero elements in a list of integers."""
  count = 0
  for x in int_list:
    if x != 0:
      count += 1
  return count

def format_output_list(int_list: List[int]) -> str:
    """Formats a list of integers into a space-separated string."""
    return " ".join(map(str, int_list))

def transform(input_str: str) -> str:
    """
    Applies the transformation rule: count non-zeros in the input string's numbers
    to determine the number of leading 1s in the output string, padding with 0s
    to match the original length.
    """
    # Parse the input string into a list of integer numbers
    input_list = parse_input_string(input_str)

    # Determine the total number of elements (length)
    n = len(input_list)
    if n == 0: # Handle empty input after parsing
        return ""

    # Count how many numbers are not zero
    c = count_non_zeros(input_list)

    # Initialize an empty list for the output numbers
    output_list = []

    # Add the required number of 1s to the output list
    output_list.extend([1] * c)

    # Add the required number of 0s to fill the remaining length
    output_list.extend([0] * (n - c))

    # Format the list of 0s and 1s back into a space-separated string
    output_str = format_output_list(output_list)

    # Return the final formatted string
    return output_str