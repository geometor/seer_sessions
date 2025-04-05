import numpy as np
import math # Note: math isn't strictly needed for this specific problem, but included as per instructions

"""
Transforms a sequence of digits by finding the first and last non-zero digits. 
All digits strictly between these two boundary digits are changed to zero, while 
the boundary digits themselves and any leading/trailing zeros remain unchanged.
"""

def find_first_non_zero_index(digit_list):
  """Finds the index of the first non-zero digit in a list."""
  for i, digit in enumerate(digit_list):
    if digit != 0:
      return i
  return None # Return None if no non-zero digit is found

def find_last_non_zero_index(digit_list):
  """Finds the index of the last non-zero digit in a list."""
  last_idx = None
  for i, digit in enumerate(digit_list):
    if digit != 0:
      last_idx = i
  return last_idx # Returns None if no non-zero digit is found, or the index of the last one

def transform(input_str):
    """
    Applies the transformation rule to the input string of digits.

    Args:
      input_str: A string of space-separated single digits.

    Returns:
      A string of space-separated single digits representing the transformed sequence.
    """
    # 1. Parse the input string into a list of digits (integers).
    input_digits = [int(d) for d in input_str.split()]

    # 2. Find the index of the first non-zero digit.
    first_idx = find_first_non_zero_index(input_digits)

    # If no non-zero digit exists, return the original string.
    if first_idx is None:
        return input_str

    # 3. Find the index of the last non-zero digit.
    #    (We know at least one exists if first_idx is not None)
    last_idx = find_last_non_zero_index(input_digits)

    # 4. Create a copy of the input list to serve as the initial output list.
    output_digits = list(input_digits) # Use list() to ensure a copy

    # 5. Iterate through the indices *between* the first and last non-zero digits.
    #    The range starts one *after* the first index and goes up to, but
    #    *not including*, the last index.
    #    If first_idx == last_idx (only one non-zero), the range will be empty.
    for i in range(first_idx + 1, last_idx):
        # Set the corresponding digit in the output list to 0.
        output_digits[i] = 0

    # 6. Convert the final output list back into a space-separated string.
    output_str = " ".join(map(str, output_digits))

    return output_str
