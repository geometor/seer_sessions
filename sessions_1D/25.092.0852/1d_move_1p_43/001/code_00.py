"""
Shift a contiguous block of non-white pixels one position to the right within a 1D sequence (single row grid), maintaining sequence length.
"""

import numpy as np

def find_first_non_white(sequence):
  """Finds the index of the first non-white pixel in a sequence."""
  for i, pixel in enumerate(sequence):
    if pixel != 0:
      return i
  return -1 # Return -1 if no non-white pixel is found (though examples suggest one always exists)

def transform(input_grid):
  """
  Transforms the input grid by shifting the non-white block one step right.

  Args:
    input_grid: A list of lists representing the input grid (expected to be 1xN).

  Returns:
    A list of lists representing the transformed grid.
  """
  # Ensure input is treated as a 1D sequence (take the first row)
  # ARC grids are list of lists, even for 1D sequences
  input_sequence = list(input_grid[0]) 
  
  # 1. Find the index of the first pixel in the sequence that is not white (color 0).
  start_index = find_first_non_white(input_sequence)

  # If no non-white block is found, return the original grid (edge case)
  if start_index == -1:
      return input_grid
      
  # 2. Create a new sequence (make a copy to avoid modifying the original list reference)
  output_sequence = list(input_sequence) 

  # 3. Insert a white pixel (0) into the new sequence at start_index.
  output_sequence.insert(start_index, 0)

  # 4. Remove the last pixel from this new sequence to maintain original length.
  output_sequence.pop() 

  # 5. The resulting sequence is the output. Format as list of lists.
  output_grid = [output_sequence] 
  
  return output_grid