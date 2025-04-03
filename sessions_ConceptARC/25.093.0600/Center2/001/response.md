```python
import collections
import math

"""
Parses a space-separated string of integers into a list.
Counts the occurrences of each integer.
Identifies the indices of integers that appear exactly once.
Finds the median index among these unique number indices (using the lower-median for even counts).
Returns the integer from the original list located at this median index.
"""

def find_unique_indices(int_list):
  """Counts numbers and returns indices of unique numbers."""
  counts = collections.Counter(int_list)
  unique_indices = []
  for i, num in enumerate(int_list):
    if counts[num] == 1:
      unique_indices.append(i)
  return unique_indices

def find_median_index_value(indices_list):
  """Calculates the median index position from a list of indices."""
  if not indices_list:
    return None # Or raise an error, depending on expected behavior for no unique numbers
  n = len(indices_list)
  # The indices are already sorted by virtue of how we collect them (iteration order)
  # We need the index *at* the median position in the indices_list
  median_position_index = (n - 1) // 2 # Integer division handles floor automatically
  return indices_list[median_position_index]

def transform(input_str: str) -> int:
  """
  Transforms the input string based on the described logic.

  Args:
    input_str: A string containing space-separated integers.

  Returns:
    The integer from the original list found at the median index 
    of the uniquely occurring numbers' indices.
  """
  # 1. Parse the input string into a list of integers.
  integer_list = [int(x) for x in input_str.split()]

  # 2. Count occurrences and identify indices of unique numbers.
  # (Helper function combines steps 2 and 3 from the natural language program)
  unique_number_indices = find_unique_indices(integer_list)

  # 4. Determine the median index from this list of indices.
  median_index_from_original_list = find_median_index_value(unique_number_indices)

  # Handle case where no unique numbers are found (though not present in examples)
  if median_index_from_original_list is None:
      # Decide on appropriate error handling or return value. 
      # For now, let's assume there's always at least one unique number based on examples.
      # If this assumption can be violated, add error handling here.
      raise ValueError("Input string does not contain any unique numbers.")


  # 5. Retrieve the integer from the original list located at this calculated median index.
  output_integer = integer_list[median_index_from_original_list]

  # 6. Output the retrieved integer.
  return output_integer

```