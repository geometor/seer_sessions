"""
Transforms a 1D NumPy array of integers based on the following rules:
1. Extracts all non-zero numbers from the input array, preserving their original relative order. These form the pool of replacement values.
2. Identifies all contiguous blocks composed solely of the number 5 within the input array.
3. Creates a copy of the input array.
4. Iterates through the identified blocks of 5s. For the k-th block (0-indexed), replaces all elements within that block's range in the copied array with the value from the replacement pool at index (k modulo the total number of replacement values).
5. If there are no non-zero numbers in the input or no blocks of 5s, the original array is returned unchanged.
6. Elements in the input array that are not part of a block of 5s retain their original values and positions in the output array.
"""
import numpy as np

def extract_replacement_values(sequence):
  """
  Extracts all non-zero elements from a NumPy array, preserving order.

  Args:
    sequence: A 1D NumPy array of integers.

  Returns:
    A 1D NumPy array containing all non-zero elements from the input sequence.
  """
  # Use boolean indexing to select elements that are not equal to 0
  return sequence[sequence != 0]

def identify_five_blocks(sequence):
  """
  Identifies contiguous blocks of the number 5 in a NumPy array.

  Args:
    sequence: A 1D NumPy array of integers.

  Returns:
    A list of tuples, where each tuple is (start_index, end_index)
    inclusive for a block of 5s. Returns an empty list if no blocks are found.
  """
  blocks = []
  in_block = False
  start_index = -1
  # Iterate through the array to find start and end points of blocks of 5s
  for i, num in enumerate(sequence):
    if num == 5 and not in_block:
      # Start of a new block
      in_block = True
      start_index = i
    elif num != 5 and in_block:
      # End of the current block (element i is the first non-5 after the block)
      blocks.append((start_index, i - 1))
      in_block = False
      start_index = -1 # Reset start index
  # Check if the sequence ends while inside a block of 5s
  if in_block:
    blocks.append((start_index, len(sequence) - 1))
  return blocks

def transform(input_array: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.
    """
    # Extract the sequence of non-zero numbers to use for replacements
    replacement_values = extract_replacement_values(input_array)

    # Identify all contiguous blocks of the number 5
    five_blocks = identify_five_blocks(input_array)

    # Create a copy of the input array to modify
    output_array = np.copy(input_array)

    # Get the number of available replacement values
    num_replacements = len(replacement_values)

    # If there are no non-zero numbers to use or no blocks of 5s to replace,
    # return the unmodified copy of the input array
    if num_replacements == 0 or not five_blocks:
      return output_array

    # Iterate through each identified block of 5s
    for block_index, (start, end) in enumerate(five_blocks):
        # Determine the replacement value, cycling through the available non-zero numbers
        # using the modulo operator on the block index
        current_replacement_value = replacement_values[block_index % num_replacements]

        # Replace all elements within the current block's range [start, end]
        # NumPy slicing allows efficient assignment to the block
        output_array[start : end + 1] = current_replacement_value

    # Return the modified array
    return output_array