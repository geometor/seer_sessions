import numpy as np
from typing import List, Union

"""
If the input sequence contains non-zero digits, extract the sub-sequence between the first and last non-zero digits (inclusive) and shift it 3 positions to the left within a sequence of 12 digits, padding the remaining positions with zeros. If the input sequence contains only zeros, the output sequence is identical to the input.
"""

def _find_first_nonzero_index(data_list: Union[List[int], np.ndarray]) -> int:
  """Finds the index of the first non-zero element."""
  for i, val in enumerate(data_list):
    if val != 0:
      return i
  return -1 # Return -1 if no non-zero element is found

def _find_last_nonzero_index(data_list: Union[List[int], np.ndarray]) -> int:
  """Finds the index of the last non-zero element."""
  last_index = -1
  # Iterate backwards for efficiency, but iterating forwards works too
  for i in range(len(data_list) - 1, -1, -1):
      if data_list[i] != 0:
          return i
  return -1 # Return -1 if no non-zero element is found

def transform(input_sequence: Union[List[int], np.ndarray]) -> List[int]:
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list or NumPy array of 12 integers.

    Returns:
        A list representing the transformed sequence of 12 integers.
    """
    # Ensure input is treated as a list for consistent indexing/slicing
    input_list = list(input_sequence)
    n = len(input_list) # Should be 12 based on examples

    # 1. Find the indices of the first and last non-zero digits
    start_index = _find_first_nonzero_index(input_list)
    
    # 2. Handle the case where the input is all zeros
    if start_index == -1:
      # If no non-zero elements, return the original sequence as a list
      return input_list

    # 3. Find the last non-zero index (only needed if there's a first one)
    end_index = _find_last_nonzero_index(input_list)

    # 4. Extract the sub-sequence
    sub_sequence = input_list[start_index : end_index + 1]
    sub_len = len(sub_sequence)

    # 5. Determine the target starting index for the output
    # Shift amount is 3 positions to the left
    shift_amount = 3
    output_start_index = start_index - shift_amount

    # 6. Create a new output list initialized with zeros
    output_list = [0] * n

    # 7. Place the extracted sub-sequence into the output list, handling boundaries
    
    # Determine the slice of the sub_sequence to copy
    source_start = 0
    source_end = sub_len
    
    # Determine the slice of the output_list to place into
    dest_start = output_start_index
    dest_end = output_start_index + sub_len

    # Adjust source slice if destination starts before index 0
    if dest_start < 0:
        source_start = -dest_start # Skip initial elements of sub_sequence
        dest_start = 0          # Start placing at index 0 in output

    # Adjust source slice if destination ends after index n-1
    if dest_end > n:
        # Calculate how much it overflows
        overflow = dest_end - n
        source_end = source_end - overflow # Don't copy the overflowing part
        dest_end = n                     # Place up to the end of the output list

    # Only perform the assignment if there's a valid range to copy/paste
    if dest_start < dest_end and source_start < source_end:
        output_list[dest_start:dest_end] = sub_sequence[source_start:source_end]

    # 8. Return the resulting output list
    return output_list