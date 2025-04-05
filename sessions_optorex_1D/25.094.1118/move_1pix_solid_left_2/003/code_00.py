import math
import numpy as np
import collections

"""
Transforms a sequence of 12 digits based on the position of the first non-zero block.

The input is assumed to be a sequence (list or 1D array) of 12 integers.
It contains a single contiguous block of identical non-zero digits, surrounded by zeros.

Transformation Rule:
1. Find the index of the first non-zero digit (`first_nz_index`).
2. If `first_nz_index` is 0 (the block starts at the beginning) or -1 (no non-zero digits found), 
   the sequence remains unchanged.
3. If `first_nz_index` is greater than 0, the zero digit immediately preceding the block 
   (at index `first_nz_index - 1`) is moved to the end of the sequence. All subsequent elements 
   shift one position to the left to fill the gap.
"""

def find_first_nonzero_index(sequence):
  """
  Finds the index of the first non-zero element in a sequence.

  Args:
      sequence: An iterable (list, tuple, numpy array) of numbers.

  Returns:
      The index of the first non-zero element, or -1 if none is found.
  """
  for i, digit in enumerate(sequence):
    # Ensure comparison is with integer 0, handling potential numpy types
    if int(digit) != 0: 
      return i
  return -1 # Indicate no non-zero element found

def transform(input_sequence):
    """
    Applies the described transformation to the input sequence.

    Args:
        input_sequence: A list or 1D numpy array of 12 integers.

    Returns:
        A list of 12 integers representing the transformed sequence.
    """
    # Ensure we are working with a standard Python list for manipulation
    # This addresses potential issues if the input is a numpy array,
    # allowing methods like .pop() and .append() to be used reliably.
    # Convert elements to int just in case they are numpy types.
    output_sequence = [int(x) for x in input_sequence]

    # Find the starting index of the non-zero block
    first_nz_index = find_first_nonzero_index(output_sequence)

    # Check the condition for transformation: block exists and doesn't start at index 0
    if first_nz_index > 0:
        # Identify the zero element immediately preceding the non-zero block
        # Remove this zero from its current position
        zero_to_move = output_sequence.pop(first_nz_index - 1)

        # Append the removed zero to the end of the sequence
        output_sequence.append(zero_to_move)
        # The sequence is now transformed

    # If first_nz_index is 0 or -1, the sequence remains unchanged
    # In this case, the original (copied) sequence is returned

    return output_sequence