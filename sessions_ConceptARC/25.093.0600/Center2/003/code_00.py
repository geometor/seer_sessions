import collections
import math
from typing import List, Union, Sequence

"""
Transforms an input list/sequence of integers based on the frequency of its elements.
1. Counts the occurrences of each integer in the input list.
2. Identifies the indices of integers that appear exactly once (unique numbers).
3. Finds the median index among the list of indices corresponding to these unique numbers. 
   If there's an even number of unique indices, the lower-median position is used 
   (index floor((n-1)/2) in the list of unique indices).
4. Returns the integer from the original input list located at this median index.
"""

def find_unique_indices(int_list: Sequence[int]) -> List[int]:
  """
  Counts numbers in the input list and returns a list of indices 
  where numbers appearing exactly once are located.

  Args:
    int_list: The input sequence of integers.

  Returns:
    A list of indices corresponding to the positions of unique numbers
    in the original list, maintaining their original relative order.
  """
  counts = collections.Counter(int_list)
  unique_indices = []
  for i, num in enumerate(int_list):
    if counts[num] == 1:
      unique_indices.append(i)
  return unique_indices

def get_value_at_median_unique_index(int_list: Sequence[int], unique_indices: List[int]) -> int:
  """
  Determines the median index from the list of unique indices and returns
  the value from the original list at that index.

  Args:
    int_list: The original input sequence of integers.
    unique_indices: A list of indices where unique numbers were found.

  Returns:
    The integer value from the original int_list located at the
    median index derived from the unique_indices list.

  Raises:
    ValueError: If the unique_indices list is empty.
    IndexError: If calculated median index is somehow out of bounds (should not happen with valid logic).
  """
  if not unique_indices:
    # Based on examples, assume at least one unique number exists.
    # If this assumption can be violated, more robust error handling or
    # a default return value might be needed.
    raise ValueError("Input list does not contain any unique numbers.")
  
  n = len(unique_indices)
  # Calculate the index corresponding to the median position within the unique_indices list.
  # Integer division (//) handles the floor operation automatically, selecting
  # the lower median index for lists with even length.
  median_position_index = (n - 1) // 2 
  
  # Retrieve the actual index from the original list stored at the median position
  # within the unique_indices list.
  target_index_in_original_list = unique_indices[median_position_index]
  
  # Return the value from the original list at that target index.
  return int_list[target_index_in_original_list]


def transform(input_list: Union[List[int], Sequence[int]]) -> int:
    """
    Processes a list or sequence of integers to find the value at the median index 
    among indices of uniquely occurring numbers.

    Args:
      input_list: A list or sequence-like object (e.g., numpy array, tuple) 
                  containing integers.

    Returns:
      The integer from the original list found at the median index 
      derived from the indices of uniquely occurring numbers.
    """

    # 1. & 2. Count occurrences and identify indices of unique numbers.
    # The helper function `find_unique_indices` performs these steps.
    unique_number_indices = find_unique_indices(input_list)

    # 3. & 4. Determine the median index from the unique indices list 
    #         and retrieve the value from the original list at that index.
    # The helper function `get_value_at_median_unique_index` performs these steps.
    output_integer = get_value_at_median_unique_index(input_list, unique_number_indices)

    # Return the final result
    return output_integer