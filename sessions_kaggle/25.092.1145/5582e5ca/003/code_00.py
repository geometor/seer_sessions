"""
Find the digit that occurs most frequently in the input NumPy array (grid),
and then create an output NumPy array of the same shape, filled entirely
with that most frequent digit.
"""

import numpy as np
import collections

def _find_most_frequent_element(arr):
  """
  Finds the most frequent element in a NumPy array.

  Args:
      arr: A NumPy array.

  Returns:
      The element that appears most frequently in the array.
      Returns None if the input array is empty.
  """
  # Flatten the array to count elements easily
  flattened_arr = arr.flatten()

  # Handle empty array case
  if flattened_arr.size == 0:
    return None

  # Count occurrences of each element
  counts = collections.Counter(flattened_arr)

  # Find the element with the highest count
  # most_common(1) returns a list like [(element, count)]
  most_frequent_element, _ = counts.most_common(1)[0]

  return most_frequent_element

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms an input grid (NumPy array) by finding the most frequent
    digit within it and creating a new grid of the same shape filled
    with that digit.

    Args:
        input_grid: A NumPy array containing digits.

    Returns:
        A NumPy array of the same shape as input_grid, filled entirely
        with the most frequent digit found in input_grid.
    """
    # Step 1 & 2: Flatten the input grid and count element frequencies
    # Step 3: Identify the most frequent digit
    most_frequent_digit = _find_most_frequent_element(input_grid)

    # Handle the case where the input grid might be empty or calculation failed
    if most_frequent_digit is None:
        # Decide behavior for empty input: return empty array of same shape? Raise error?
        # For now, return an empty array matching input shape if possible.
        # If input_grid itself was None or unshaped, this might need more robust handling.
        # However, based on examples, input is always a populated grid.
        # Let's assume valid input and proceed. If input can be empty, add checks.
        # A simple approach for non-empty grid guarantee:
         pass # Continue, as None case implies empty grid which shouldn't happen based on examples


    # Step 4: Determine the shape of the input grid
    grid_shape = input_grid.shape

    # Step 5, 6 & 7: Construct and fill the output grid
    # Create a new NumPy array with the same shape as the input
    # and fill it with the most frequent digit.
    # Ensure the dtype matches the most frequent digit's type if necessary,
    # though np.full often handles this reasonably.
    output_grid = np.full(grid_shape, most_frequent_digit, dtype=input_grid.dtype)

    # Step 8: Return the newly constructed grid
    return output_grid