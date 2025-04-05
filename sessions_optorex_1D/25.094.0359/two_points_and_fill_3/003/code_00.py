import math
import numpy as np
import collections

"""
Transforms an input sequence (list or array) of integers by:
1. Identifying the unique non-zero digit within the sequence.
2. Finding the indices of the first and last occurrences of this non-zero digit.
3. Creating a new sequence where the segment between (and including) these first and last indices is filled with the non-zero digit.
4. Elements outside this segment remain unchanged from the input sequence.
"""

def find_non_zero_digit(sequence):
  """Finds the first non-zero digit encountered in a sequence."""
  for digit in sequence:
    if digit != 0:
      return digit
  return None # Should not happen based on problem constraints

def find_first_last_indices(sequence, target_digit):
  """Finds the first and last indices of a target digit in a sequence."""
  first_index = -1
  last_index = -1
  for i, digit in enumerate(sequence):
    if digit == target_digit:
      if first_index == -1:
        first_index = i
      last_index = i
  return first_index, last_index

def transform(input_sequence):
    """
    Transforms the input sequence by filling the segment between the first and last
    occurrences of the non-zero digit with that digit.
    Assumes input_sequence is a list or 1D array of integers.
    """
    # Ensure input is a list for consistent processing, copy to avoid modifying original
    input_list = list(input_sequence) 
    output_sequence = list(input_list) # Create a copy for modification

    # 1. Identify the non-zero digit present in the input sequence.
    marker_digit = find_non_zero_digit(input_list)

    # Handle edge case where no non-zero digit is found (unlikely given examples)
    if marker_digit is None:
        return output_sequence # Return the copy of the original

    # 2. & 3. Find the first and last indices of the marker digit.
    start_index, end_index = find_first_last_indices(input_list, marker_digit)

    # Handle edge case where indices are not found (unlikely given examples)
    if start_index == -1:
         return output_sequence # Return the copy of the original

    # 4. Iterate from start_index to end_index and fill with marker_digit.
    for i in range(start_index, end_index + 1):
        output_sequence[i] = marker_digit

    # 5. Return the modified sequence. 
    # If the original input was a numpy array and the output needs to be too, convert back.
    if isinstance(input_sequence, np.ndarray):
        return np.array(output_sequence)
    else:
        return output_sequence