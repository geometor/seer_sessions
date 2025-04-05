"""
Receive an input sequence of 12 integers.
Divide the input sequence into two parts: the first 8 integers (Part A) and the last 4 integers (Part B).
Create the output sequence by concatenating Part B followed by Part A.
"""

import numpy as np # Although not strictly needed for this task, included as per general instructions

# Helper function (though simple, illustrates the concept)
def split_and_concatenate(sequence, split_index):
  """
  Splits a sequence at a given index and concatenates the second part followed by the first.

  Args:
    sequence: The input list or sequence.
    split_index: The index at which to split the sequence. The first part will
                 contain elements up to (but not including) this index.

  Returns:
    A new list formed by concatenating the part after the split index
    with the part before the split index.
  """
  part_a = sequence[:split_index] # Elements from start up to split_index
  part_b = sequence[split_index:] # Elements from split_index to end
  return part_b + part_a

def transform(input_list):
  """
  Transforms the input sequence of 12 integers by moving the last 4 elements
  to the beginning.

  Args:
    input_list: A list of 12 integers (received typically from parsing the input string).

  Returns:
    A list of 12 integers representing the transformed sequence.
  """

  # Define the split point based on the observation (first 8 elements form one part)
  # The split happens *after* the 8th element, so the index is 8.
  split_at = 8

  # Use the helper function to perform the split and concatenation
  # The function takes the input list and the index where the second part begins.
  output_list = split_and_concatenate(input_list, split_at)

  # Return the resulting list
  return output_list

# Example usage (based on train_1):
# Assuming the input string "0 1 9 5 4 2 5 6 4 2 0 0" is parsed into a list first:
# input_data = [0, 1, 9, 5, 4, 2, 5, 6, 4, 2, 0, 0]
# transformed_data = transform(input_data)
# print(transformed_data) # Output should be [4, 2, 0, 0, 0, 1, 9, 5, 4, 2, 5, 6]