"""
Transforms an input sequence of integers based on the count of its non-zero elements.
The rule is:
1. Count the number of non-zero elements in the input sequence (N).
2. Determine the total length of the input sequence (L).
3. Construct an output sequence containing N ones followed by (L - N) zeros.
4. Return the resulting sequence.
"""

import numpy as np

def count_non_zeros_in_sequence(sequence):
  """Counts the number of non-zero elements in a sequence (list or array)."""
  count = 0
  for element in sequence:
    if element != 0:
      count += 1
  return count

def transform(input_sequence):
    """
    Transforms an input sequence of integers by replacing it with a sequence
    of 1s (equal to the count of non-zero elements in the input) followed by 0s.

    Args:
        input_sequence: A list or numpy array of integers.

    Returns:
        A numpy array of integers representing the transformed sequence.
    """
    # Ensure input is treated as a numpy array for consistency, though list works too
    if not isinstance(input_sequence, np.ndarray):
        input_sequence = np.array(input_sequence)

    # Determine the total length of the input sequence
    total_length = len(input_sequence)

    # Count the number of non-zero elements in the input sequence
    non_zero_count = count_non_zeros_in_sequence(input_sequence)

    # Calculate the number of zeros needed for the output sequence
    zero_count = total_length - non_zero_count

    # Construct the output sequence: N ones followed by (L - N) zeros
    # Create a list first
    output_list = [1] * non_zero_count + [0] * zero_count

    # Convert the output list to a numpy array
    output_sequence = np.array(output_list)

    return output_sequence
