import math
import numpy as np

"""
Takes a sequence of integers represented as a space-separated string. 
Separates the zero elements from the non-zero elements.
Constructs a new sequence where all the zero elements from the input are placed at the beginning, 
followed by all the non-zero elements from the input, maintaining their original relative order.
Returns the resulting sequence as a space-separated string.
"""

def parse_input(input_str):
  """Converts a space-separated string of integers into a list of integers."""
  return [int(x) for x in input_str.split()]

def format_output(output_list):
  """Converts a list of integers into a space-separated string."""
  return " ".join(map(str, output_list))

def separate_zeros_nonzeros(int_list):
  """Separates a list of integers into two lists: one for zeros and one for non-zeros."""
  zeros = [x for x in int_list if x == 0]
  non_zeros = [x for x in int_list if x != 0]
  return zeros, non_zeros

def transform(input_str):
  """
  Applies the transformation rule: moves all zeros to the left and non-zeros to the right,
  preserving the relative order of non-zeros.
  """
  # Parse the input string into a list of integers
  input_list = parse_input(input_str)

  # Separate the list into zeros and non-zeros
  # The relative order of non-zeros is preserved by list comprehension
  zeros, non_zeros = separate_zeros_nonzeros(input_list)

  # Construct the output list by concatenating the zeros list and the non-zeros list
  # This places all zeros first, followed by non-zeros in their original relative order
  output_list = zeros + non_zeros

  # Format the output list back into a space-separated string
  output_str = format_output(output_list)

  return output_str

# Example usage (based on train_1)
# input_example = "0 0 9 0 0 8 0 0 0 0 0 0"
# output_example = transform(input_example)
# print(f"Input: {input_example}")
# print(f"Output: {output_example}")
# Expected: 0 0 0 0 0 0 0 0 0 0 9 8