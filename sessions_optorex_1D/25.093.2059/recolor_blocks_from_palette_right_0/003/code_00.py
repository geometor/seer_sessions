"""
Transforms a sequence of integers by replacing consecutive sequences of '5's.
The replacement value for the k-th sequence of '5's is determined by the k-th 
non-zero number found in the original input sequence. Non-zero numbers 
(including the replacement values) and zeros retain their original positions 
unless they are part of a '5' sequence being replaced.
"""

import numpy as np
import re # Although re was used before for string splitting, it's not needed if input is an array

def get_replacement_pool(numbers):
  """
  Extracts all non-zero numbers from a list or array, preserving order.

  Args:
    numbers: A list or NumPy array of integers.

  Returns:
    A list of non-zero integers in their original order.
  """
  # Ensure we are working with a list or iterable
  if isinstance(numbers, np.ndarray):
      numbers = numbers.tolist()
  pool = [num for num in numbers if num != 0]
  return pool

def find_five_sequences(numbers):
    """
    Identifies consecutive sequences of the number 5.

    Args:
        numbers: A list or NumPy array of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a sequence
        and contains 'start_index' and 'length'.
        Example: [{'start_index': 4, 'length': 3}, {'start_index': 9, 'length': 3}]
    """
    if isinstance(numbers, np.ndarray):
        numbers = numbers.tolist() # Work with list for easier iteration

    sequences = []
    i = 0
    while i < len(numbers):
        if numbers[i] == 5:
            start_index = i
            length = 0
            # Count consecutive 5s
            while i < len(numbers) and numbers[i] == 5:
                length += 1
                i += 1
            sequences.append({'start_index': start_index, 'length': length})
        else:
            # Move to the next number if it's not a 5
            i += 1
    return sequences


def transform(input_data):
    """
    Applies the transformation rule to the input sequence (NumPy array).

    Args:
        input_data: A NumPy array of integers.

    Returns:
        A NumPy array with sequences of 5s replaced according to the rule.
    """
    # Ensure input is a NumPy array for consistency, make a copy to modify
    if not isinstance(input_data, np.ndarray):
        # If input is list or other, convert for consistency, though problem description implies ndarray
        input_grid = np.array(input_data)
    else:
        input_grid = input_data.copy() # Work on a copy

    output_grid = input_grid.copy() # Initialize output as a copy of input

    # 1. Get the pool of replacement values (all non-zero numbers from original input)
    replacement_pool = get_replacement_pool(input_grid)

    # 2. Find all consecutive sequences of 5s in the original input
    five_sequences = find_five_sequences(input_grid)

    # 3. Iterate through the sequences of 5s and apply replacements
    pool_idx = 0 # Index for the replacement pool
    for seq in five_sequences:
        if pool_idx < len(replacement_pool):
            # Get the replacement value from the pool
            replacement_value = replacement_pool[pool_idx]

            # Get sequence details
            start = seq['start_index']
            length = seq['length']

            # Replace the 5s in the output grid
            for i in range(start, start + length):
                output_grid[i] = replacement_value

            # Move to the next replacement value in the pool
            pool_idx += 1
        else:
            # Optional: Handle cases where there are more 5-sequences than pool numbers
            # Based on examples, this doesn't seem to happen, or if it did,
            # the remaining 5s might be left unchanged.
            # Current logic leaves them unchanged as output_grid was initialized from input_grid.
            # print(f"Warning: Ran out of replacement values in the pool for sequence starting at index {seq['start_index']}.")
            break # Stop processing if pool is exhausted

    return output_grid