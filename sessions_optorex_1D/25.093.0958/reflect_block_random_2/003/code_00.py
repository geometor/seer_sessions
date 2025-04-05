import numpy as np
import math # Not strictly needed, but included as per template request
import collections # Not strictly needed, but potentially useful for sequence analysis

"""
Transforms a sequence (list or NumPy array) of single-digit integers.
The transformation identifies the contiguous sub-sequence bounded by the first and last non-zero digits (inclusive).
This sub-sequence is then reversed in place, while any leading and trailing zeros remain in their original positions.
If the sequence contains only zeros, it remains unchanged.
"""

def _find_first_non_zero_index(int_list):
  """Finds the index of the first non-zero element in a list or 1D array."""
  for i, val in enumerate(int_list):
    if val != 0:
      return i
  return -1 # Indicates no non-zero element found

def _find_last_non_zero_index(int_list):
  """Finds the index of the last non-zero element in a list or 1D array."""
  # Iterate backwards to find the last non-zero element efficiently
  for i in range(len(int_list) - 1, -1, -1):
    if int_list[i] != 0:
      return i
  return -1 # Indicates no non-zero element found

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the described transformation to the input NumPy array.

    Args:
        input_grid: A 1D NumPy array containing single-digit integers.

    Returns:
        A 1D NumPy array containing the transformed sequence.
    """
    # Assume input_grid is a 1D NumPy array based on previous error context.
    # If it could be a list, convert it: input_list = list(input_grid)
    # However, operating directly on NumPy arrays is usually more efficient.

    # 1. Find the index of the first non-zero integer.
    start_index = _find_first_non_zero_index(input_grid)

    # 2. Handle the case where the input contains only zeros.
    if start_index == -1:
      # If no non-zero element found, return the original grid unchanged.
      return input_grid.copy() # Return a copy to avoid modifying the original input if it's mutable

    # 3. Find the index of the last non-zero integer.
    # We know at least one non-zero exists if start_index != -1.
    end_index = _find_last_non_zero_index(input_grid)

    # 4. Extract the three components using NumPy slicing.
    # a. Leading part (before the first non-zero)
    leading_part = input_grid[:start_index]
    # b. Middle part (from first non-zero to last non-zero, inclusive)
    middle_part = input_grid[start_index : end_index + 1]
    # c. Trailing part (after the last non-zero)
    trailing_part = input_grid[end_index + 1:]

    # 5. Reverse the order of the integers within the middle part.
    reversed_middle_part = middle_part[::-1] # Efficient slicing for reversal

    # 6. Construct the output sequence by concatenating the parts.
    # np.concatenate requires a tuple or list of arrays.
    output_grid = np.concatenate((leading_part, reversed_middle_part, trailing_part))

    # 7. Return the constructed NumPy array.
    return output_grid