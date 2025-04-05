```python
import math
import numpy as np
import collections

"""
Transforms a sequence of 12 integers by counting the non-zero elements 
and creating an output sequence of 12 integers with that many '1's 
grouped at the end, preceded by '0's.
"""

def count_non_zero(input_list):
  """Counts the number of non-zero elements in a list."""
  count = 0
  for item in input_list:
    if item != 0:
      count += 1
  return count

def transform(input_str):
    """
    Transforms an input string of 12 space-separated integers based on the count of non-zero elements.

    Args:
        input_str: A string containing 12 space-separated integers.

    Returns:
        list: A list of 12 integers (0s and 1s) where the number of 1s
              equals the count of non-zero elements in the input, and the
              1s are grouped at the end of the list.
    """
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_str.split()]

    # Count the non-zero elements in the input list
    non_zero_count = count_non_zero(input_list)

    # Determine the length of the sequence (assumed to be 12 based on examples)
    sequence_length = len(input_list)
    
    # Initialize the output list with zeros
    output_list = [0] * sequence_length

    # Calculate the starting index for the ones
    # If non_zero_count is 0, start_index will be sequence_length, and the loop below won't run.
    start_index = sequence_length - non_zero_count 

    # Fill the end of the output list with ones
    for i in range(start_index, sequence_length):
        output_list[i] = 1
        
    return output_list

```