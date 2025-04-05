"""
Counts the non-zero integers in the input sequence/array. Let this count be N. 
Generates an output sequence/array of length 12 containing N integers 
with the value 1, followed by 12 - N integers with the value 0.
"""

import numpy as np

def count_non_zeros(sequence):
  """Counts the number of non-zero elements in a sequence (list or numpy array)."""
  # Use numpy's efficient count_nonzero for arrays, otherwise iterate
  if isinstance(sequence, np.ndarray):
      return np.count_nonzero(sequence)
  else:
      count = 0
      for item in sequence:
          if item != 0:
              count += 1
      return count

def generate_output_sequence(length, num_ones):
  """Generates a numpy array of 1s followed by 0s."""
  # Create an array of zeros
  output = np.zeros(length, dtype=int)
  # Set the first num_ones elements to 1
  output[:num_ones] = 1
  return output

def transform(input_sequence):
    """
    Transforms an input sequence (list or NumPy array) of 12 integers 
    into an output sequence of 1s and 0s based on the count of 
    non-zero input integers.
    """
    
    # Assume the input is a sequence (like list or numpy array)
    # Define the fixed length of the sequences
    sequence_length = 12 # Or len(input_sequence) if it can vary, but examples show 12
    
    # Count the non-zero elements in the input sequence
    non_zero_count = count_non_zeros(input_sequence)
    
    # Generate the output sequence based on the count
    output_sequence = generate_output_sequence(sequence_length, non_zero_count)
    
    # Return the resulting sequence (as a numpy array for consistency)
    return output_sequence