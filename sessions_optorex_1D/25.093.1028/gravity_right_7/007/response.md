```python
import numpy as np # Although not strictly necessary for this logic, keeping for potential compatibility
import math
import re # Although not used, keeping for consistency

"""
Rearranges a sequence of digits by moving all zero (0) elements to the beginning of the sequence, while preserving the original relative order of all non-zero elements.
"""

def partition_by_value(sequence, value_to_partition):
  """
  Partitions a sequence into two lists based on whether elements equal a specific value.

  Args:
      sequence: The input list or array-like sequence.
      value_to_partition: The value to check for partitioning (e.g., 0).

  Returns:
      A tuple containing two lists: (elements_equal_to_value, elements_not_equal_to_value).
      The relative order within each list is preserved.
  """
  elements_equal = []
  elements_not_equal = []
  for element in sequence:
      if element == value_to_partition:
          elements_equal.append(element)
      else:
          elements_not_equal.append(element)
  return elements_equal, elements_not_equal

def transform(input_sequence):
    """
    Moves all zeros in the input sequence to the beginning, preserving the relative order of non-zero elements.

    Args:
        input_sequence: A list or array-like sequence of integers (digits 0-9).

    Returns:
        A new list containing the rearranged sequence of digits.
    """

    # 1. Partition the input sequence into zeros and non-zeros.
    #    Use a helper function to separate elements based on the value 0,
    #    while preserving the relative order within the non-zero group.
    zeros_group, non_zeros_group = partition_by_value(input_sequence, 0)

    # 2. Concatenate the partitioned groups.
    #    Combine the list of zeros followed by the list of non-zeros.
    output_sequence = zeros_group + non_zeros_group

    # 3. Return the rearranged sequence.
    return output_sequence
```