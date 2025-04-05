```python
import collections

"""
Transforms an input sequence (list of integers) by keeping only the longest
contiguous block for each non-zero number present in the sequence. All other
occurrences of those non-zero numbers are replaced with 0. Zeros in the
original sequence remain zero unless they are part of the longest block of a
non-zero number (which is implicitly handled by overwriting). If multiple
blocks of the same number share the maximum length, the one occurring earliest
(lowest start index) is chosen.
"""

def find_blocks(data, value):
  """Finds all contiguous blocks of a specific value in the data list.

  Args:
    data: A list of integers.
    value: The integer value to search for blocks of.

  Returns:
    A list of dictionaries, where each dictionary represents a block
    and contains 'value', 'start', 'end', and 'length'.
    Returns an empty list if the value is 0 or no blocks are found.
  """
  # Block finding is only relevant for non-zero values
  if value == 0:
    return []

  blocks = []
  start_index = -1
  # Iterate through the list with index
  for i, element in enumerate(data):
    # Check if the current element matches the target value
    if element == value:
      # If this is the start of a new block, record the index
      if start_index == -1:
        start_index = i
    # If the element does not match and we were inside a block
    elif start_index != -1:
      # The block has just ended, record its details
      blocks.append({
          'value': value,
          'start': start_index,
          'end': i - 1, # The block ended at the previous index
          'length': (i - 1) - start_index + 1 # Calculate length
      })
      # Reset start_index to indicate we are no longer in a block
      start_index = -1

  # After the loop, check if we were inside a block when the list ended
  if start_index != -1:
    blocks.append({
        'value': value,
        'start': start_index,
        'end': len(data) - 1, # Block ends at the last index
        'length': (len(data) - 1) - start_index + 1 # Calculate length
    })

  return blocks

def find_longest_block(blocks):
  """Finds the block with the maximum length from a list of blocks.

  Args:
    blocks: A list of block dictionaries (from find_blocks).

  Returns:
    The block dictionary with the maximum length, or None if the list is empty.
    If multiple blocks share the max length, the first one encountered
    (which corresponds to the earliest start index due to the nature of
    find_blocks) is returned because max() is stable.
  """
  if not blocks:
    return None
  # Use max with a key function to find the block with the largest 'length'
  # max() in Python is stable, so it returns the first element in case of ties
  # Since blocks are found left-to-right, this correctly handles the tie-breaking rule.
  return max(blocks, key=lambda b: b['length'])


def transform(input_list):
  """
  Applies the transformation rule to the input list.

  Args:
    input_list: A list of integers representing the input sequence.

  Returns:
    A new list of integers representing the transformed sequence.
  """
  # Get the length of the input list
  n = len(input_list)

  # Initialize the output list with zeros, same length as input
  output_list = [0] * n

  # Identify unique non-zero values in the input list
  # Using a set handles duplicates, list() converts it, sorted() ensures order (optional but good practice)
  unique_non_zeros = sorted(list(set(val for val in input_list if val != 0)))

  # Process each unique non-zero value found
  for value in unique_non_zeros:
    # Find all contiguous blocks of the current value in the input
    current_blocks = find_blocks(input_list, value)

    # If blocks were found for this value
    if current_blocks:
      # Find the longest block among them (handles tie-breaking)
      longest = find_longest_block(current_blocks)

      # If a longest block exists (should always be true if current_blocks is not empty)
      if longest:
        # Iterate through the indices covered by the longest block
        for i in range(longest['start'], longest['end'] + 1):
          # Set the corresponding position in the output list to the block's value
          output_list[i] = longest['value'] # or simply `value`

  # Return the final transformed list
  return output_list
```