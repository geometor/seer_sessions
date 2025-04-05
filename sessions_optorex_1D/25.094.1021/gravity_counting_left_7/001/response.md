```python
import math
import numpy as np
import collections

"""
Transform an input sequence of single-digit integers into a binary sequence of the same length.
The output sequence consists of a block of zeros followed by a block of ones.
The number of zeros in the output sequence is equal to the total count of the digit '0' in the input sequence.
The remaining positions in the output sequence are filled with ones.
"""

def count_occurrences(sequence, value):
  """Counts the occurrences of a specific value in a sequence."""
  count = 0
  for item in sequence:
    if item == value:
      count += 1
  return count

def transform(input_str: str) -> str:
    """
    Transforms an input string of space-separated digits into a binary string based on the count of zeros.

    Args:
        input_str: A string containing space-separated single-digit integers.

    Returns:
        A string containing space-separated binary digits (0 or 1).
    """
    # Parse the input string into a list of integers
    input_sequence = [int(digit) for digit in input_str.split()]

    # Count the total number of times the digit '0' appears
    zero_count = count_occurrences(input_sequence, 0)
    # Alternatively using list.count: zero_count = input_sequence.count(0)

    # Determine the length of the input sequence
    length = len(input_sequence)

    # Initialize the output sequence
    output_sequence = []

    # Generate the output sequence
    # Iterate through the indices from 0 up to length - 1
    for i in range(length):
      # If the index is less than the count of zeros, append 0
      if i < zero_count:
        output_sequence.append(0)
      # Otherwise, append 1
      else:
        output_sequence.append(1)

    # Format the output sequence as a space-separated string
    output_str = " ".join(map(str, output_sequence))

    return output_str

```