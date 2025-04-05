"""
Transforms an input sequence of integers into an output sequence of binary digits (0s and 1s) of the same length. The number of leading '1's in the output sequence corresponds directly to the total count of non-zero integers found in the input sequence. The remaining elements of the output sequence are '0's.
"""

import numpy as np

def count_non_zeros(sequence):
  """Counts the number of non-zero elements in a sequence."""
  count = 0
  for element in sequence:
    if element != 0:
      count += 1
  return count

def transform(input_str):
  """
  Applies the transformation rule to the input string.

  Args:
    input_str: A string containing space-separated integers.

  Returns:
    A string containing space-separated binary digits representing the transformed output.
  """
  # Parse the input string into a list of integers
  input_list = [int(x) for x in input_str.split()]
  input_length = len(input_list)

  # Count the non-zero elements in the input list
  non_zero_count = count_non_zeros(input_list)

  # Initialize the output list with zeros
  output_list = [0] * input_length

  # Set the first 'non_zero_count' elements to 1
  for i in range(non_zero_count):
      # Check bounds just in case, though logic implies it won't exceed
      if i < input_length:
          output_list[i] = 1

  # Format the output list back into a space-separated string
  output_str = " ".join(map(str, output_list))

  return output_str
