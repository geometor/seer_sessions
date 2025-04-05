```python
import math
import numpy as np

"""
Constructs a binary sequence based on an input integer sequence.
The length of the output sequence is the same as the input sequence.
The number of '1's at the beginning of the output sequence equals the count of non-zero elements in the input sequence.
The remaining elements of the output sequence are '0's.
"""

def count_non_zeros(int_list):
  """Counts the number of non-zero elements in a list of integers."""
  count = 0
  for x in int_list:
    if x != 0:
      count += 1
  return count

def parse_input_string(input_str):
  """Parses a space-separated string into a list of integers."""
  return [int(s) for s in input_str.split()]

def format_output_list(int_list):
    """Formats a list of integers into a space-separated string."""
    return " ".join(map(str, int_list))

def transform(input_str: str) -> str:
    """
    Transforms an input string of space-separated integers into an output string
    of space-separated binary digits (0s and 1s). The number of 1s in the output
    corresponds to the count of non-zero numbers in the input.
    """
    # Parse the input string into a list of integers
    input_list = parse_input_string(input_str)

    # Get the total length of the input sequence
    n = len(input_list)

    # Count the number of non-zero elements in the input sequence
    c = count_non_zeros(input_list)

    # Initialize the output list
    output_list = []

    # Add 'c' number of 1s to the output list
    for _ in range(c):
        output_list.append(1)

    # Add 'n - c' number of 0s to the output list
    for _ in range(n - c):
        output_list.append(0)

    # Format the output list into a space-separated string
    output_str = format_output_list(output_list)

    return output_str

```