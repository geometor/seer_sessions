```python
import sys
import math
# Add imports if needed, e.g.:
# import numpy as np
# import re

"""
Sorts a sequence of space-separated integers (0, 1, 2) in non-decreasing order.
"""

def parse_input(input_str):
  """
  Parses a string of space-separated integers into a list of integers.
  """
  return [int(x) for x in input_str.split()]

def format_output(int_list):
  """
  Formats a list of integers into a space-separated string.
  """
  return " ".join(map(str, int_list))

def transform(input_str):
    """
    Takes a string of space-separated integers, sorts them numerically,
    and returns the sorted sequence as a space-separated string.
    """

    # 1. Parse the input string into a list of integer values.
    #    Example: "2 1 0 2" -> [2, 1, 0, 2]
    int_list = parse_input(input_str)

    # 2. Sort this list/array of integers in non-decreasing (ascending) numerical order.
    #    Example: [2, 1, 0, 2] -> [0, 1, 2, 2]
    sorted_list = sorted(int_list)

    # 3. Format the sorted list/array back into a string with integers separated by single spaces.
    #    Example: [0, 1, 2, 2] -> "0 1 2 2"
    output_str = format_output(sorted_list)

    # 4. Return the resulting string.
    return output_str

```