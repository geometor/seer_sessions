"""
Transforms a 1D NumPy array of digits by finding the indices of the first and last 
non-zero elements. All elements strictly between these two boundary indices are 
changed to zero, while the boundary elements themselves and any elements outside 
this range (leading/trailing zeros) remain unchanged. If there are no non-zero 
elements or only one, the array remains unchanged.
"""

import numpy as np
import math # Note: math isn't strictly needed for this specific problem

def find_non_zero_indices(arr):
  """Finds the indices of all non-zero elements in a 1D NumPy array."""
  # np.where returns a tuple of arrays, one for each dimension. 
  # Since the input is 1D, we take the first element of the tuple.
  indices = np.where(arr != 0)[0] 
  return indices

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input 1D NumPy array.

    Args:
      input_grid: A 1D NumPy array of integer digits.

    Returns:
      A 1D NumPy array representing the transformed sequence.
    """
    # 1. Find the indices of all non-zero elements.
    non_zero_indices = find_non_zero_indices(input_grid)

    # 2. If no non-zero elements exist (or implicitly if only one exists, 
    #    as the slicing range below will be empty), return a copy of the original.
    if len(non_zero_indices) < 2:
        return input_grid.copy() # Return a copy to avoid modifying the original input

    # 3. Determine the index of the first non-zero element.
    first_idx = np.min(non_zero_indices)

    # 4. Determine the index of the last non-zero element.
    last_idx = np.max(non_zero_indices)

    # 5. Create a copy of the input array to serve as the output array.
    output_grid = input_grid.copy()

    # 6. Select the slice of the output array strictly between the first 
    #    and last non-zero indices.
    # 7. Set all elements within this slice to 0.
    #    NumPy slicing `[start:end]` includes `start` but excludes `end`.
    #    So `first_idx + 1` starts after the first non-zero element,
    #    and `last_idx` stops before the element at last_idx.
    output_grid[first_idx + 1 : last_idx] = 0

    # 8. Return the modified output array.
    return output_grid