import numpy as np

"""
Transforms an input sequence of 12 integers into an output sequence of 12 binary digits (0s and 1s). The number of '1's in the output sequence is equal to the count of non-zero integers in the input sequence. The '1's appear at the beginning of the output sequence, followed by '0's to complete the sequence length of 12.
"""

def count_non_zeros(data_sequence):
  """Counts the number of non-zero elements in a sequence (list or NumPy array)."""
  # Use numpy's count_nonzero for efficiency if it's an array,
  # otherwise iterate for lists.
  if isinstance(data_sequence, np.ndarray):
    return np.count_nonzero(data_sequence)
  else:
    count = 0
    for item in data_sequence:
      if item != 0:
        count += 1
    return count

def transform(input_sequence):
  """
  Applies the transformation rule to the input sequence.

  Args:
    input_sequence: A sequence (list or NumPy array) of 12 integers.

  Returns:
    A NumPy array of 12 binary integers (0s and 1s).
  """
  # Ensure the input is treated as a NumPy array for consistency
  # Although the helper function handles lists, the environment likely uses NumPy.
  if not isinstance(input_sequence, np.ndarray):
      input_sequence = np.array(input_sequence)

  # 1. Count the number of non-zero elements in the input sequence.
  non_zero_count = count_non_zeros(input_sequence)

  # 2. Determine the total length (should always be 12 based on examples).
  total_length = len(input_sequence) # Or assume 12 directly

  # 3. Calculate the number of zeros needed.
  zero_count = total_length - non_zero_count

  # 4. Create the output sequence: 'non_zero_count' ones followed by 'zero_count' zeros.
  # Using NumPy makes this construction straightforward.
  output_ones = np.ones(non_zero_count, dtype=int)
  output_zeros = np.zeros(zero_count, dtype=int)
  output_sequence = np.concatenate((output_ones, output_zeros))

  # 5. Return the generated output sequence.
  return output_sequence