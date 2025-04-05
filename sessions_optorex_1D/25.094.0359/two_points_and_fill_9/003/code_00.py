"""
Transforms a 1D NumPy array of digits by identifying the first and last occurrences 
of a non-zero digit and filling the segment between them (inclusive) with that digit.
Elements outside this segment remain unchanged. If no non-zero digits are present, 
the array is returned unchanged.
"""

import numpy as np

def find_non_zero_indices(grid):
  """Finds the indices of all non-zero elements in a 1D NumPy array."""
  # np.nonzero returns a tuple of arrays, one for each dimension. 
  # For a 1D array, we take the first element of the tuple.
  return np.nonzero(grid)[0] 

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the segment filling transformation to a 1D NumPy array.

    Args:
        input_grid: A 1D NumPy array containing integers.

    Returns:
        A 1D NumPy array containing the transformed sequence.
    """
    
    # Find the indices of all non-zero elements.
    non_zero_indices = find_non_zero_indices(input_grid)

    # If there are no non-zero elements, return a copy of the original grid.
    if len(non_zero_indices) == 0:
        return input_grid.copy()

    # Identify the fill value (the non-zero digit).
    # It's guaranteed by the problem description that only one non-zero digit exists.
    # We can take the value from the first non-zero element found.
    fill_value = input_grid[non_zero_indices[0]] 

    # Find the start and end indices of the segment to fill.
    # These are the minimum and maximum indices of the non-zero elements.
    start_index = np.min(non_zero_indices)
    end_index = np.max(non_zero_indices)

    # Initialize the output grid as a copy of the input grid.
    output_grid = input_grid.copy()

    # Fill the segment from start_index to end_index (inclusive) with the fill_value.
    # NumPy slicing [start:end+1] includes the element at end index.
    output_grid[start_index : end_index + 1] = fill_value

    return output_grid