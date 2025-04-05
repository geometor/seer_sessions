import numpy as np
import collections

"""
Transforms an input sequence (NumPy array) of integers based on the most frequent non-zero digit.

1.  Receive the input sequence as a NumPy array of integers.
2.  Create a list containing only the non-zero integers from the input sequence.
3.  If this list of non-zero integers is empty (meaning the input sequence contained only zeros or was empty), return a copy of the original input sequence.
4.  If there are non-zero integers, count the occurrences of each unique non-zero integer in the list.
5.  Determine the non-zero integer that occurs most frequently (the mode).
6.  Create a copy of the input sequence to serve as the basis for the output sequence.
7.  Iterate through each element and its index in the input sequence:
    *   If the element is non-zero, replace the element at the corresponding index in the output sequence with the mode determined in step 5.
    *   If the element is zero, leave the element at the corresponding index in the output sequence unchanged (it will remain zero from the copy).
8.  Return the modified output sequence (NumPy array).
"""

def find_non_zero_mode(numbers):
  """
  Finds the most frequent non-zero number in a NumPy array or list.
  Returns None if no non-zero numbers exist or the input is empty.
  """
  # Extract non-zero elements using numpy indexing if it's an array
  if isinstance(numbers, np.ndarray):
      non_zeros = numbers[numbers != 0]
      # Convert to list for Counter compatibility if needed, though Counter works with arrays too
      # Using list() is slightly more robust if array contains non-hashable types later,
      # but for integers, it's fine either way. Let's stick to array for efficiency.
      if non_zeros.size == 0:
          return None
  else: # Assume list-like
      non_zeros = [n for n in numbers if n != 0]
      if not non_zeros:
        return None

  # Count occurrences of each non-zero number
  counts = collections.Counter(non_zeros)
  
  # Find the number with the maximum count.
  # most_common(1) returns a list containing one tuple: [(mode, count)]
  mode, _ = counts.most_common(1)[0]
  return mode

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input numpy array.
    """
    # Find the mode of the non-zero elements
    mode_digit = find_non_zero_mode(input_grid)

    # If there are no non-zero elements (mode is None), return the original grid unchanged
    if mode_digit is None:
      return np.copy(input_grid) # Return a copy to avoid modifying the original input

    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)

    # Replace all non-zero elements with the mode digit using boolean indexing
    # This efficiently applies the change without an explicit loop
    output_grid[output_grid != 0] = mode_digit

    return output_grid