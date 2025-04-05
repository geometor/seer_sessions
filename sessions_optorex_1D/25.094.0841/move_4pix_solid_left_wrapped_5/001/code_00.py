import numpy as np
import collections

"""
Transforms the input sequence by interpreting it as a 3x4 grid (row-major order)
and performing a circular upward shift of the rows by one position. The first
row moves to the last position, and all other rows shift up. The resulting grid
is then flattened back into a sequence.
"""

def reshape_to_grid(sequence, rows, cols):
  """Reshapes a flat sequence into a 2D grid (list of lists)."""
  if len(sequence) != rows * cols:
    raise ValueError("Sequence length does not match grid dimensions")
  grid = []
  for i in range(rows):
    start_index = i * cols
    end_index = start_index + cols
    grid.append(list(sequence[start_index:end_index]))
  return grid

def flatten_grid(grid):
  """Flattens a 2D grid (list of lists) into a flat sequence."""
  return [item for sublist in grid for item in sublist]

def shift_rows_up(grid):
  """Performs a circular upward shift on the rows of the grid."""
  if not grid:
    return []
  # Use collections.deque for efficient rotation
  rows_deque = collections.deque(grid)
  rows_deque.rotate(-1) # Negative rotation shifts elements to the left (upward)
  return list(rows_deque)

def transform(input_sequence):
    """
    Applies the row-shifting transformation to the input sequence.

    Args:
        input_sequence: A list of 12 integers.

    Returns:
        A list of 12 integers representing the transformed sequence.
    """
    # Define grid dimensions
    rows = 3
    cols = 4

    # Reshape the input sequence into a 3x4 grid
    # Example: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] ->
    # [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    input_grid = reshape_to_grid(input_sequence, rows, cols)

    # Perform the circular upward shift on the rows
    # Example: [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]] ->
    # [[5, 6, 7, 8], [9, 10, 11, 12], [1, 2, 3, 4]]
    shifted_grid = shift_rows_up(input_grid)

    # Flatten the resulting grid back into a sequence
    # Example: [[5, 6, 7, 8], [9, 10, 11, 12], [1, 2, 3, 4]] ->
    # [5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4]
    output_sequence = flatten_grid(shifted_grid)

    return output_sequence
