"""
Transforms a 1D NumPy array of digits by identifying the first and last occurrences 
of a non-zero digit and filling the segment between them (inclusive) with that digit.
Elements outside this segment remain unchanged. If no non-zero digits are present, 
the array is returned unchanged.
"""

import numpy as np

def find_non_zero_indices(grid: np.ndarray) -> np.ndarray:
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
    
    # Find the indices of all elements in the list/array that are not zero.
    non_zero_indices = find_non_zero_indices(input_grid)

    # If there are no non-zero elements, return the original grid unchanged (make a copy).
    if len(non_zero_indices) == 0:
        return input_grid.copy()

    # If there are non-zero elements:
    
    # Identify the value of the non-zero digit (`fill_value`).
    # Since all non-zero elements have the same value (as per task examples),
    # pick the value from the first non-zero element found.
    fill_value = input_grid[non_zero_indices[0]] 

    # Determine the smallest index (`start_index`) where a non-zero element occurs.
    start_index = np.min(non_zero_indices)
    
    # Determine the largest index (`end_index`) where a non-zero element occurs.
    end_index = np.max(non_zero_indices)

    # Create a new array as a copy of the input to avoid modifying the original.
    output_grid = input_grid.copy()

    # Modify the copied array: For every index `i` from `start_index` up to 
    # and including `end_index`, set the element at index `i` to `fill_value`.
    # NumPy slicing [start:end+1] selects the range including the end index.
    output_grid[start_index : end_index + 1] = fill_value

    # Return the modified grid.
    return output_grid