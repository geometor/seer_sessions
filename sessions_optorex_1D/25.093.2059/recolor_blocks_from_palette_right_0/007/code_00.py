"""
Transforms a sequence of integers represented by a NumPy array. 
The transformation rule involves identifying consecutive sequences of the integer '5'. 
Each such sequence (found sequentially from left to right) is replaced by a 
corresponding value taken from an ordered 'replacement pool'. This pool is 
constructed by extracting all non-zero, non-5 integers from the original input 
sequence, maintaining their relative order. The k-th sequence of '5's is 
replaced by the k-th value from the replacement pool, repeated for the length 
of the sequence. If there are more sequences of '5's than available values 
in the replacement pool, the remaining sequences of '5's are left unchanged. 
All other numbers (zeros and the original non-zero, non-5 numbers) retain 
their original positions in the output.
"""

import numpy as np

def get_replacement_pool(numbers):
  """
  Extracts non-zero numbers, excluding 5, from a NumPy array, preserving order.

  Args:
    numbers: A NumPy array of integers.

  Returns:
    A list of non-zero, non-5 integers in their original order.
  """
  # Filter out 0s and 5s, convert to list of standard Python ints
  pool = [int(num) for num in numbers if num != 0 and num != 5]
  return pool

def find_five_sequences(numbers):
    """
    Identifies consecutive sequences of the number 5 in a NumPy array.

    Args:
        numbers: A NumPy array of integers.

    Returns:
        A list of dictionaries, where each dictionary represents a sequence
        and contains 'start_index' (int) and 'length' (int). Sequences are
        ordered as they appear in the input array.
        Example: [{'start_index': 4, 'length': 3}, {'start_index': 9, 'length': 3}]
    """
    sequences = []
    i = 0
    n = len(numbers)
    while i < n:
        # Check if the current number is 5
        if numbers[i] == 5:
            start_index = i
            length = 0
            # Count consecutive 5s from the current position
            while i < n and numbers[i] == 5:
                length += 1
                i += 1
            # Record the sequence found using standard Python ints
            sequences.append({'start_index': int(start_index), 'length': int(length)})
        else:
            # Move to the next number if it's not a 5
            i += 1
    return sequences


def transform(input_grid):
    """
    Applies the transformation rule to the input sequence (NumPy array).

    Args:
        input_grid: A NumPy array of integers representing the input sequence.

    Returns:
        A NumPy array with sequences of 5s replaced according to the rule.
    """
    # Ensure input is a NumPy array
    if not isinstance(input_grid, np.ndarray):
        input_grid_np = np.array(input_grid)
    else:
        input_grid_np = input_grid # Avoid unnecessary copy if already np array

    # Initialize output_grid as a copy of the input grid to preserve original values
    output_grid = input_grid_np.copy()

    # 1. Build the replacement pool (non-zero, non-5 numbers) from the original input
    replacement_pool = get_replacement_pool(input_grid_np)

    # 2. Find all consecutive sequences of 5s in the original input
    five_sequences = find_five_sequences(input_grid_np)

    # 3. Iterate through the sequences of 5s and apply replacements
    # Determine how many replacements can be made (limited by the shorter of the two lists)
    num_replacements = min(len(five_sequences), len(replacement_pool))

    # Loop through the sequences that have a corresponding replacement value
    for k in range(num_replacements):
        # Get the details of the k-th sequence of 5s
        seq = five_sequences[k]
        start = seq['start_index']
        length = seq['length']

        # Get the k-th replacement value from the pool
        replacement_value = replacement_pool[k]

        # Replace the slice in the output grid corresponding to the 5s sequence
        # Using NumPy array slicing for efficient assignment
        output_grid[start : start + length] = replacement_value

    # Sequences of 5s for which k >= num_replacements are left untouched
    # because output_grid started as a copy of input_grid.
    # Zeros and the original non-zero, non-5 numbers are also preserved from the copy.

    return output_grid