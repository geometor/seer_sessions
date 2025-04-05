import numpy as np
import re

"""
Transforms an input sequence of space-separated integers by identifying the block 
containing all elements from the first non-zero integer to the last non-zero 
integer (inclusive), and shifting this entire block two positions to the right 
within a sequence of zeroes of the same original length. If the input contains 
only zeroes, the output is identical to the input.
"""

def _find_first_nonzero_index(int_list):
  """Finds the index of the first non-zero element."""
  for i, x in enumerate(int_list):
    if x != 0:
      return i
  return -1 # Indicate not found

def _find_last_nonzero_index(int_list):
  """Finds the index of the last non-zero element."""
  for i in range(len(int_list) - 1, -1, -1):
    if int_list[i] != 0:
      return i
  return -1 # Indicate not found

def transform(input_str: str) -> str:
    """
    Applies the block shifting transformation to the input string.

    Args:
        input_str: A string of space-separated integers.

    Returns:
        A string of space-separated integers representing the transformed sequence.
    """
    # 1. Parse the input string into a list of integers.
    input_list = [int(x) for x in input_str.split()]
    n = len(input_list)

    # 2. Find the index of the first non-zero integer.
    first_nz_idx = _find_first_nonzero_index(input_list)

    # 3. Handle the edge case where no non-zero integers are present.
    if first_nz_idx == -1:
        # Return the original string (or an equivalent string of zeros)
        return input_str

    # 4. Find the index of the last non-zero integer.
    last_nz_idx = _find_last_nonzero_index(input_list) # We know at least one exists

    # 5. Extract the sub-list (the "block").
    active_block = input_list[first_nz_idx : last_nz_idx + 1]

    # 6. Create a new list of the original length, filled entirely with zeroes.
    output_list = [0] * n

    # 7. Calculate the target starting index and place the block.
    target_start_idx = first_nz_idx + 2
    target_end_idx = target_start_idx + len(active_block)

    # Ensure the block placement doesn't exceed the list bounds
    # (Though the examples suggest this won't happen with the +2 shift)
    if target_end_idx <= n:
        output_list[target_start_idx:target_end_idx] = active_block
    # else: handle potential out-of-bounds - current examples don't require this

    # 8. Format the resulting list back into a string.
    output_str = " ".join(map(str, output_list))

    return output_str
