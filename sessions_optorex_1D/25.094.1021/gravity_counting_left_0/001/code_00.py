import numpy as np

"""
Transforms an input list of 12 integers into an output list of 12 binary integers (0s and 1s). 
The output list consists of a sequence of 0s followed by a sequence of 1s.
The index where the sequence transitions from 0 to 1 is determined by subtracting 
the count of non-zero elements in the input list from the total length (12).
"""

def count_non_zeros(data_list):
  """Counts the number of non-zero elements in a list."""
  count = 0
  for item in data_list:
    if item != 0:
      count += 1
  return count

def transform(input_list):
    """
    Applies the transformation rule to the input list.

    Args:
      input_list: A list of 12 integers.

    Returns:
      A list of 12 binary integers (0s and 1s).
    """
    # Ensure input is treated as a list or 1D array
    # The examples provide space-separated strings, implying a 1D structure.
    # If the input is intended as a grid, it needs clarification, but based on examples,
    # we treat it as a flat list of 12 numbers.
    if not isinstance(input_list, list):
         # Simple parsing if input is a string like the examples
         if isinstance(input_list, str):
              input_list = [int(x) for x in input_list.split()]
         else:
              # Attempt conversion if possible, e.g., from numpy array
              try:
                  input_list = list(np.array(input_list).flatten())
              except Exception as e:
                  raise TypeError(f"Input type {type(input_list)} not directly usable. Expected list or compatible type. Error: {e}")

    list_length = 12
    if len(input_list) != list_length:
        raise ValueError(f"Input list must have exactly {list_length} elements.")

    # 1. Count the number of non-zero elements in the input list.
    non_zero_count = count_non_zeros(input_list)

    # 2. Calculate the transition index k.
    # k is the index where 1s start, which is also the count of initial 0s.
    transition_index = list_length - non_zero_count

    # 3. Create the output list.
    # Initialize with all zeros.
    output_list = [0] * list_length

    # 4. Set elements from the transition index onwards to 1.
    for i in range(transition_index, list_length):
        output_list[i] = 1

    return output_list