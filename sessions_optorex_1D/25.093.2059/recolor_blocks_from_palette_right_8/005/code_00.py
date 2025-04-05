import math

def get_replacement_values(sequence):
  """Extracts all non-zero numbers from a sequence, preserving order."""
  return [num for num in sequence if num != 0]

def find_target_five_blocks(sequence):
  """
  Identifies contiguous blocks of two or more 5s in a sequence.

  Args:
    sequence: A list of integers.

  Returns:
    A list of tuples, where each tuple is (start_index, end_index)
    inclusive for a block of 5s with length >= 2.
  """
  blocks = []
  in_block = False
  start_index = -1
  count = 0
  for i, num in enumerate(sequence):
    if num == 5:
      if not in_block:
        # Potentially starting a block
        in_block = True
        start_index = i
        count = 1
      else:
        # Continuing a block
        count += 1
    elif num != 5:
      # Element is not 5, check if we were in a block
      if in_block:
        # Check if the block we just exited was long enough
        if count >= 2:
          blocks.append((start_index, i - 1))
        # Reset block tracking
        in_block = False
        start_index = -1
        count = 0
  # After the loop, check if we ended inside a valid block
  if in_block and count >= 2:
    blocks.append((start_index, len(sequence) - 1))
  return blocks

def transform(input_sequence):
  """
  Transforms the input sequence according to the following rule:
  1. Identify all non-zero numbers in the input sequence, maintaining their relative order (replacement values).
  2. Identify all contiguous blocks consisting of two or more '5's (target blocks).
  3. Replace the elements of the k-th target block with the (k modulo N)-th replacement value, where N is the total number of replacement values.
  4. Numbers not part of a target block remain unchanged.
  """

  # Step 1: Get the pool of values to use for replacement
  replacement_values = get_replacement_values(input_sequence)

  # Step 2: Find the blocks of '55' or longer to be replaced
  target_blocks = find_target_five_blocks(input_sequence)

  # Initialize the output sequence as a copy of the input
  # Use list() to ensure it's a mutable copy, not just a reference
  output_sequence = list(input_sequence)

  # Step 3: Perform the replacements
  # Check if there are replacement values and blocks to replace
  num_replacements = len(replacement_values)
  if num_replacements == 0 or not target_blocks:
    # Nothing to replace, return the original sequence copy
    return output_sequence

  # Iterate through the identified target blocks
  for block_index, (start, end) in enumerate(target_blocks):
    # Determine the replacement value, cycling through the replacement pool
    # Use modulo operator for cycling
    current_replacement_value = replacement_values[block_index % num_replacements]

    # Replace all elements within the current target block's range
    for i in range(start, end + 1):
      output_sequence[i] = current_replacement_value

  # Step 4: Return the modified sequence
  return output_sequence