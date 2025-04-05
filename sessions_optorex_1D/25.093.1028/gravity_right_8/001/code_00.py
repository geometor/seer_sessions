import math
import collections

"""
Processes a space-separated string of digits. It rearranges the digits such that all '0's appear first, followed by all non-zero digits. The relative order of the non-zero digits is preserved from the input string.
"""

def parse_input_string(input_str):
  """Converts a space-separated string of digits into a list of strings."""
  return input_str.split(' ')

def filter_digits(digit_list):
  """Separates a list of digit strings into two lists: zeros and non-zeros."""
  zeros = []
  non_zeros = []
  for digit in digit_list:
    if digit == '0':
      zeros.append(digit)
    else:
      non_zeros.append(digit)
  return zeros, non_zeros

def format_output_string(digit_list):
  """Joins a list of digit strings into a single space-separated string."""
  return ' '.join(digit_list)

def transform(input_str):
  """
  Rearranges digits in a space-separated string, placing all zeros at the beginning
  while preserving the relative order of non-zero digits.

  Args:
    input_str: A string containing space-separated digits.

  Returns:
    A string with digits rearranged according to the rule.
  """
  # 1. Parse the input string into a list of individual digits (as strings).
  input_digits = parse_input_string(input_str)

  # 2 & 3 & 4. Filter the digits into two lists: one for zeros and one for non-zeros,
  # maintaining the order for non-zeros.
  zeros_list, non_zeros_list = filter_digits(input_digits)

  # 5. Combine the list of zeros followed by the list of non-zeros.
  rearranged_digits = zeros_list + non_zeros_list

  # 6. Convert the rearranged list back into a space-separated string.
  output_str = format_output_string(rearranged_digits)

  return output_str
