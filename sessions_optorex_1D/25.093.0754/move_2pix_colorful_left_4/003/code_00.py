"""
Transforms an input sequence of 12 integers by identifying the block of elements from the first non-zero to the last non-zero (inclusive) and shifting this block two positions to the left. The sequence is padded with zeros to maintain its original length of 12. If the input sequence contains only zeros, it is returned unchanged.
"""

import numpy as np # Using numpy for potentially easier index finding, though list methods are also viable

def _find_non_zero_indices(sequence):
  """Finds the indices of non-zero elements in a sequence."""
  # Using numpy.where which returns a tuple of arrays (one for each dimension)
  non_zero_indices = np.where(np.array(sequence) != 0)[0]
  if len(non_zero_indices) == 0:
    return None, None # No non-zero elements found
  return non_zero_indices[0], non_zero_indices[-1]

def transform(input_sequence):
  """
  Applies the described transformation to the input sequence.

  Args:
    input_sequence: A list of 12 integers.

  Returns:
    A list of 12 integers representing the transformed sequence.
  """
  sequence_length = len(input_sequence) # Typically 12 based on examples

  # 1. Find the indices of the first and last non-zero elements
  first_nz_index_in, last_nz_index_in = _find_non_zero_indices(input_sequence)

  # 2. Handle the all-zeros case
  if first_nz_index_in is None:
    return list(input_sequence) # Return a copy to avoid modifying original if it matters

  # 3. Extract the non-zero block
  # Slice from the first non-zero index up to and including the last non-zero index
  non_zero_block = input_sequence[first_nz_index_in : last_nz_index_in + 1]
  block_length = len(non_zero_block)

  # 4. Calculate the target starting index for the block in the output
  # The shift is consistently 2 positions to the left
  shift_amount = 2
  first_nz_index_out = first_nz_index_in - shift_amount

  # Ensure the output index is not negative (though examples suggest it won't be)
  if first_nz_index_out < 0:
      # This case shouldn't happen based on observed examples, but handling defensively
      print(f"Warning: Calculated output start index {first_nz_index_out} is negative. Adjusting.")
      # Decide on behavior: clip block? shift less? error?
      # Based on task structure, it implies sufficient leading zeros exist.
      # If it *could* happen, logic needs clarification. Assuming it doesn't for now.
      first_nz_index_out = 0 # Example adjustment: place at start if shift goes too far left

  # 5. Create the output sequence initialized with zeros
  output_sequence = [0] * sequence_length

  # 6. Place the extracted non-zero block into the output sequence
  # Calculate the end index for slicing in the output sequence
  end_index_out = first_nz_index_out + block_length
  
  # Ensure the block fits within the sequence length
  if end_index_out > sequence_length:
      # Also shouldn't happen based on examples (implies trailing zeros exist)
      print(f"Warning: Calculated output end index {end_index_out} exceeds sequence length {sequence_length}. Truncating block.")
      # Adjust block or indices if necessary
      output_sequence[first_nz_index_out:] = non_zero_block[:sequence_length - first_nz_index_out]
  else:
       output_sequence[first_nz_index_out:end_index_out] = non_zero_block

  # 7. Return the constructed output sequence
  return output_sequence
