import numpy as np
import collections.abc # To check for sequence types

"""
Transforms an input sequence of 12 integers based on the count of non-zero elements.

The process involves:
1. Ensuring the input, regardless of its initial format (string, list, numpy array),
   is converted into a flat list of 12 integers.
2. Counting the number of elements in this flattened list that are not equal to 0. Let this count be 'k'.
3. Constructing an output list of length 12, consisting of '12 - k' zeros followed by 'k' ones.
"""

def _flatten_and_convert_to_int_list(sequence):
  """
  Converts various input types (string, list, numpy array) into a flat list of integers.

  Args:
    sequence: The input sequence (string, list, tuple, numpy array).

  Returns:
    A flat list of integers.

  Raises:
    ValueError: If the input cannot be reliably converted or doesn't contain 12 elements.
  """
  flat_list = []
  if isinstance(sequence, str):
      # Input is a space-separated string
      try:
          flat_list = [int(x) for x in sequence.split()]
      except ValueError as e:
          raise ValueError(f"Could not convert string elements to integers: {e}")
  elif isinstance(sequence, np.ndarray):
      # Input is a numpy array, flatten it and convert to list
      flat_list = [int(x) for x in sequence.flatten()]
  elif isinstance(sequence, collections.abc.Sequence):
      # Input is a list or tuple, attempt to flatten (handles nested lists/tuples)
      def flatten(l):
          for el in l:
              if isinstance(el, collections.abc.Iterable) and not isinstance(el, (str, bytes)):
                  yield from flatten(el)
              else:
                  try:
                      yield int(el)
                  except (ValueError, TypeError) as e:
                      raise ValueError(f"Could not convert element '{el}' to integer: {e}")
      flat_list = list(flatten(sequence))
  else:
      raise TypeError(f"Unsupported input type: {type(sequence)}")

  # Validate length
  if len(flat_list) != 12:
      raise ValueError(f"Input sequence must contain exactly 12 elements after flattening, found {len(flat_list)}")

  return flat_list


def count_non_zeros(int_list):
  """Counts the number of non-zero elements in a list of integers."""
  count = 0
  for element in int_list:
    # Ensure comparison is valid (already converted to int)
    if element != 0:
      count += 1
  return count

def transform(input_sequence):
  """
  Applies the transformation rule to the input sequence.

  Args:
    input_sequence: A representation of 12 integers (string, list, tuple, numpy array).

  Returns:
    A list of 12 integers (0s and 1s) representing the transformed sequence.
  """
  # Step 1 & 2: Flatten input and convert to a list of integers
  try:
      flat_int_list = _flatten_and_convert_to_int_list(input_sequence)
  except (ValueError, TypeError) as e:
      # Handle potential errors during conversion/flattening
      print(f"Error processing input: {e}")
      # Return a default or raise the error, depending on desired behavior
      # Returning a default list of zeros for robustness in this context
      return [0] * 12

  # Step 3 & 4 & 5: Count non-zero elements
  non_zero_count = count_non_zeros(flat_int_list)

  # Step 6: Define sequence length
  sequence_length = 12

  # Step 7 & 8: Create the output sequence
  # Calculate the number of zeros
  num_zeros = sequence_length - non_zero_count
  # Ensure num_zeros is not negative (if somehow non_zero_count > 12)
  num_zeros = max(0, num_zeros)
  # Construct the output list
  output_sequence = [0] * num_zeros + [1] * non_zero_count

  # Step 9: Return the result
  return output_sequence
