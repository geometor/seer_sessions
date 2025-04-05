"""
Transforms an input sequence of integers by identifying contiguous blocks (runs)
of each unique non-zero value. For each unique non-zero value, only the single
block with the maximum length is preserved in the output. If multiple blocks
share the maximum length for a given value, the block that appears earliest
(smallest start index) in the input sequence is chosen. All elements
corresponding to non-selected blocks, and all original zero elements that are
not part of a selected block, become zero in the output sequence. The output
sequence has the same length as the input sequence.
"""

import collections # Not strictly required but potentially useful for variations

def find_blocks(data, value):
  """Finds all contiguous blocks of a specific non-zero value in the data list.

  Args:
    data: A list of integers.
    value: The non-zero integer value to search for blocks of.

  Returns:
    A list of dictionaries, where each dictionary represents a block
    and contains 'value', 'start', 'end', and 'length'.
    Returns an empty list if no blocks are found.
  """
  # Assumes value is non-zero as per the main logic calling this function
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
      end_index = i - 1
      blocks.append({
          'value': value,
          'start': start_index,
          'end': end_index,
          'length': end_index - start_index + 1
      })
      # Reset start_index to indicate we are no longer in a block
      start_index = -1

  # After the loop, check if we were inside a block when the list ended
  if start_index != -1:
    end_index = len(data) - 1
    blocks.append({
        'value': value,
        'start': start_index,
        'end': end_index,
        'length': end_index - start_index + 1
    })

  return blocks

def select_target_block(blocks):
  """Selects the target block based on length (max) and start index (min tie-breaker).

  Args:
    blocks: A list of block dictionaries (from find_blocks).

  Returns:
    The single selected block dictionary, or None if the list is empty.
  """
  if not blocks:
    return None

  # Use max with a key function prioritizing length, then minimizing start index
  # max(iterable, key=lambda x: (primary_sort_key, secondary_sort_key, ...))
  # We want max length (primary) and min start index (secondary).
  # To use max() for the secondary key (min start index), we maximize the negative start index.
  return max(blocks, key=lambda b: (b['length'], -b['start']))


def transform(input_list):
    """
    Applies the transformation rule to the input list.

    Args:
      input_list: A list of integers representing the input sequence.
                  (Note: uses input_list for clarity over template's input_grid).

    Returns:
      A new list of integers representing the transformed sequence.
    """
    # Determine the length of the input sequence
    n = len(input_list)

    # Create an output sequence of length N, initialized entirely with zeros.
    # This serves as the base, only selected blocks will overwrite zeros.
    output_list = [0] * n

    # Identify the set of unique non-zero integer values present in the input sequence.
    # Using a set automatically handles duplicates. Sorting ensures consistent processing order (optional but good practice).
    unique_non_zeros = sorted(list(set(val for val in input_list if val != 0)))

    # Process each unique non-zero value found in the input
    for value in unique_non_zeros:
      # Find all contiguous blocks (runs) of the current value 'V' in the input sequence.
      current_blocks = find_blocks(input_list, value)

      # Proceed only if blocks were found for this value
      if current_blocks:
        # Select the single target block: longest, then earliest start index.
        selected_block = select_target_block(current_blocks)

        # If a block was selected (should always be true if current_blocks is not empty)
        if selected_block:
          # Iterate through the indices covered by the selected block.
          for i in range(selected_block['start'], selected_block['end'] + 1):
            # Set the element at index 'i' in the *output* sequence to the block's value.
            output_list[i] = selected_block['value'] # or simply `value`

    # Return the generated output sequence.
    return output_list