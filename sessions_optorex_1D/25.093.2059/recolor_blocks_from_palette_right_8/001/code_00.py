import math

def extract_non_zeros(sequence):
  """Extracts all non-zero integers from a sequence, preserving order."""
  return [num for num in sequence if num != 0]

def identify_five_blocks(sequence):
  """Identifies contiguous blocks of the number 5 in a sequence.

  Args:
    sequence: A list of integers.

  Returns:
    A list of tuples, where each tuple is (start_index, end_index)
    inclusive for a block of 5s.
  """
  blocks = []
  in_block = False
  start_index = -1
  for i, num in enumerate(sequence):
    if num == 5 and not in_block:
      # Start of a new block
      in_block = True
      start_index = i
    elif num != 5 and in_block:
      # End of the current block
      blocks.append((start_index, i - 1))
      in_block = False
      start_index = -1
  # Check if the sequence ends with a block of 5s
  if in_block:
    blocks.append((start_index, len(sequence) - 1))
  return blocks

def transform(input_sequence):
  """
  Transforms the input sequence based on the following rules:
  1. Extracts all non-zero numbers from the input sequence, preserving their order.
  2. Identifies contiguous blocks of the number 5 in the input sequence.
  3. Replaces each block of 5s sequentially with the extracted non-zero numbers,
     cycling through the non-zero numbers if there are more blocks than non-zero numbers.
  4. Numbers other than 5 remain unchanged in their original positions.
  """

  # Extract the non-zero numbers to use as replacement values
  non_zero_numbers = extract_non_zeros(input_sequence)

  # Identify the blocks of 5s that need replacement
  five_blocks = identify_five_blocks(input_sequence)

  # Initialize the output sequence as a copy of the input
  output_sequence = list(input_sequence) # Create a mutable copy

  # If there are no non-zero numbers or no blocks of 5s, no replacements are needed
  if not non_zero_numbers or not five_blocks:
    return output_sequence

  # Iterate through the identified blocks of 5s and replace them
  num_replacements = len(non_zero_numbers)
  for block_index, (start, end) in enumerate(five_blocks):
      # Determine the replacement value using modulo arithmetic for cycling
      replacement_value = non_zero_numbers[block_index % num_replacements]

      # Replace all 5s within the current block's range
      for i in range(start, end + 1):
          output_sequence[i] = replacement_value

  return output_sequence