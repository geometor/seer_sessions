"""
Counts the non-zero integers in the input sequence. Let this count be N. 
Generates an output sequence containing N integers with the value 1, 
followed by 12 - N integers with the value 0.
"""

import math
import numpy as np
# No specific libraries needed beyond basic list operations

def count_non_zeros(sequence):
  """Counts the number of non-zero elements in a list of numbers."""
  count = 0
  for item in sequence:
    if item != 0:
      count += 1
  return count

def generate_output_sequence(length, num_ones):
  """Generates a sequence of 1s followed by 0s."""
  output = [1] * num_ones + [0] * (length - num_ones)
  return output

def transform(input_str):
    """
    Transforms an input string of space-separated integers into an output string 
    of 1s and 0s based on the count of non-zero input integers.
    """
    
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_str.split()]
    
    # Define the fixed length of the sequences
    sequence_length = 12 
    
    # Count the non-zero elements in the input list
    non_zero_count = count_non_zeros(input_list)
    
    # Generate the output sequence based on the count
    output_list = generate_output_sequence(sequence_length, non_zero_count)
    
    # Format the output list back into a space-separated string
    output_str = " ".join(map(str, output_list))

    return output_str
