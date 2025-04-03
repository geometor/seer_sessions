"""
Transforms an input NumPy array of 12 integers by rotating the sequence 2 positions to the left. The first two elements of the input array are moved to the end of the sequence.
"""

import numpy as np

def rotate_left_np(sequence, positions):
  """
  Rotates a NumPy array to the left by a specified number of positions.

  Args:
    sequence: The input NumPy array.
    positions: The number of positions to rotate left.

  Returns:
    The rotated NumPy array.
  """
  if sequence is None or sequence.size == 0 or positions <= 0:
    return sequence # No rotation needed or possible

  effective_positions = positions % sequence.size # Handle rotations larger than array length
  if effective_positions == 0:
      return sequence # No effective rotation

  # Slice the array into two parts using NumPy slicing
  part_to_move = sequence[:effective_positions]
  remaining_part = sequence[effective_positions:]

  # Concatenate the parts in the new order using np.concatenate
  rotated_sequence = np.concatenate((remaining_part, part_to_move))
  return rotated_sequence

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies a left rotation transformation to the input NumPy array.

    Args:
      input_grid: A 1D NumPy array of integers (shape (12,)).

    Returns:
      A 1D NumPy array representing the transformed sequence.
    """

    # Define the rotation amount based on the observed pattern.
    rotation_amount = 2

    # Perform the left rotation using the helper function.
    # This takes the elements from index `rotation_amount` to the end,
    # and concatenates them with the elements from the beginning up to
    # (but not including) index `rotation_amount`.
    output_grid = rotate_left_np(input_grid, rotation_amount)

    # Return the resulting NumPy array.
    return output_grid