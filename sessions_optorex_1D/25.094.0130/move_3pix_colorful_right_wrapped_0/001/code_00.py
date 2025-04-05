"""
Transforms an input sequence of 12 numbers by performing a right circular shift of 3 positions.
The last 3 elements of the input sequence are moved to the beginning, followed by the first 9 elements.
"""

import numpy as np
import math

def parse_input_string(input_str):
  """Converts a space-separated string of numbers into a list of integers."""
  return [int(x) for x in input_str.split()]

def format_output_list(output_list):
  """Converts a list of integers back into a space-separated string."""
  return " ".join(map(str, output_list))

def right_circular_shift(sequence, shift_amount):
  """Performs a right circular shift on a list."""
  if not sequence:
    return []
  shift = shift_amount % len(sequence) # Ensure shift is within bounds
  # Slice the last 'shift' elements and the first 'len(sequence) - shift' elements
  last_elements = sequence[-shift:]
  first_elements = sequence[:-shift]
  # Concatenate them in the new order
  return last_elements + first_elements

def transform(input_str):
  """
  Applies a right circular shift of 3 positions to the input sequence.

  Args:
    input_str: A string containing 12 space-separated integers.

  Returns:
    A string containing the transformed sequence, space-separated.
  """
  # 1. Parse the input string into a list of numbers.
  input_sequence = parse_input_string(input_str)

  # Check if the input sequence has the expected length (optional but good practice)
  if len(input_sequence) != 12:
      # Handle error or unexpected input length if necessary
      # For this specific task based on examples, we assume 12 elements.
      pass

  # 2. Perform the right circular shift by 3 positions.
  #    - Identify the last 3 elements.
  #    - Identify the first 9 elements.
  #    - Concatenate last 3 followed by first 9.
  shift_amount = 3
  output_sequence = right_circular_shift(input_sequence, shift_amount)

  # 3. Format the resulting list back into a space-separated string.
  output_str = format_output_list(output_sequence)

  return output_str
