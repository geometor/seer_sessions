import numpy as np

"""
Rotate the input sequence of 12 integers cyclically to the left by 3 positions.
The first 3 elements of the input sequence become the last 3 elements of the
output sequence. The elements from index 3 to 11 of the input sequence become
the elements from index 0 to 8 of the output sequence.
"""

def rotate_left(sequence, amount):
  """
  Rotates a sequence (list or numpy array) cyclically to the left by a given amount.

  Args:
    sequence: The input list or numpy array.
    amount: The number of positions to rotate left.

  Returns:
    The rotated sequence (same type as input).
  """
  if len(sequence) == 0:
      return sequence
  amount = amount % len(sequence) # Ensure amount is within bounds

  # Slice the sequence into two parts: the part to move to the end, and the part to move to the front
  part_to_move_to_end = sequence[:amount]
  part_to_move_to_front = sequence[amount:]

  # Concatenate the parts in the new order
  if isinstance(sequence, np.ndarray):
    # Use np.concatenate for numpy arrays
    rotated_sequence = np.concatenate((part_to_move_to_front, part_to_move_to_end))
  else:
    # Use list concatenation for lists
    rotated_sequence = part_to_move_to_front + part_to_move_to_end

  return rotated_sequence

def transform(input_sequence):
  """
  Applies a left cyclic rotation by 3 positions to the input sequence.

  Args:
    input_sequence: A list or numpy array representing a sequence of 12 integers.

  Returns:
    A list or numpy array representing the rotated sequence.
  """

  # Define the rotation amount
  rotation_amount = 3

  # Perform the left rotation using the helper function
  output_sequence = rotate_left(input_sequence, rotation_amount)

  return output_sequence