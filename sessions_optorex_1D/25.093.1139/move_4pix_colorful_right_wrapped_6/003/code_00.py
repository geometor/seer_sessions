"""
Receive the input sequence of 12 integers.
Identify the first 8 integers as Part A.
Identify the last 4 integers as Part B.
Construct the output sequence by concatenating Part B followed by Part A.
"""

import numpy as np # numpy might be implicitly used by the framework or useful for array operations

# Helper function for the core rearrangement logic
def split_and_rotate(sequence, split_index):
  """
  Splits a sequence at a given index and concatenates the second part followed by the first.

  Args:
    sequence: The input list or sequence.
    split_index: The index defining the split. The first part includes elements
                 from index 0 up to (but not including) split_index. The second
                 part includes elements from split_index to the end.

  Returns:
    A new list formed by concatenating the part after the split index
    with the part before the split index.
  """
  # Ensure the input is a standard Python list for slicing
  if isinstance(sequence, np.ndarray):
      # If it's a numpy array, flatten it and convert to list
      # Assuming it's either 1D or effectively 1D (like 1xN or Nx1)
      sequence_list = sequence.flatten().tolist()
  elif isinstance(sequence, list):
      sequence_list = sequence
  else:
      # Attempt conversion for other sequence types, might need adjustment
      sequence_list = list(sequence)

  if not sequence_list:
      return [] # Handle empty input

  # Perform the split and concatenation
  part_a = sequence_list[:split_index] # Elements from start up to split_index
  part_b = sequence_list[split_index:] # Elements from split_index to end
  
  return part_b + part_a

def transform(input_grid):
    """
    Transforms a 1D input sequence (represented as input_grid) by moving the
    last 4 elements to the beginning.

    Args:
      input_grid: Expected to be a list or numpy array representing the 1x12 sequence.

    Returns:
      A list representing the transformed 1x12 sequence.
    """

    # Define the index where the split occurs.
    # We want the last 4 elements, which means the split happens after the 8th element.
    # In 0-based indexing, the 8th element is at index 7. The split point is index 8.
    split_point = 8

    # Apply the split and rotation logic using the helper function
    # Pass the input_grid directly, the helper will handle list/numpy conversion
    output_sequence = split_and_rotate(input_grid, split_point)

    # The framework might expect a specific format (e.g., numpy array).
    # Since the previous run failed on output, let's return a standard list first.
    # If issues persist, we might need to return np.array(output_sequence) or reshape.
    return output_sequence