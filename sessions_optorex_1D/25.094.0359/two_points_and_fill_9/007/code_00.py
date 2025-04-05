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
    
    # Step 1 & 2: Find all indices where the element is non-zero.
    non_zero_indices = find_non_zero_indices(input_grid)

    # Step 3: Check for non-zero values.
    if len(non_zero_indices) == 0:
        # If no non-zero values are found, return the original grid unchanged (as a copy).
        return input_grid.copy()

    # Step 4: Determine the fill value.
    # Since all non-zero elements have the same value (as per task examples),
    # pick the value from the first non-zero element found.
    fill_value = input_grid[non_zero_indices[0]] 

    # Step 5: Determine the segment boundaries.
    # Find the smallest index (`start_index`) where a non-zero element occurs.
    start_index = np.min(non_zero_indices)
    # Find the largest index (`end_index`) where a non-zero element occurs.
    end_index = np.max(non_zero_indices)

    # Step 6: Create the output sequence (start with a copy).
    output_grid = input_grid.copy()

    # Step 7: Fill the segment.
    # Modify the copied array: For every index `i` from `start_index` up to 
    # and including `end_index`, set the element at index `i` to `fill_value`.
    # NumPy slicing [start:end+1] selects the range including the end index.
    output_grid[start_index : end_index + 1] = fill_value

    # Step 8: Output the modified sequence.
    return output_grid