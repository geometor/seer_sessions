import numpy as np

"""
Transforms an input 1D NumPy integer array by identifying the block containing 
all elements from the first non-zero integer to the last non-zero integer 
(inclusive), and shifting this entire block two positions to the right within 
a new array of zeroes of the same original length. If the input array contains 
only zeroes, the output is identical to the input.
"""

def _find_first_last_nonzero_indices(arr):
  """
  Finds the indices of the first and last non-zero elements in a 1D NumPy array.

  Args:
      arr: The input 1D NumPy array.

  Returns:
      A tuple (first_idx, last_idx). Returns (-1, -1) if no non-zero elements are found.
  """
  # Find indices where elements are non-zero
  nz_indices = np.nonzero(arr)[0] 
  if nz_indices.size == 0:
      # Handle case with no non-zero elements
      return -1, -1 
  else:
      # Return the minimum and maximum index found
      return nz_indices.min(), nz_indices.max()

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the block shifting transformation to the input NumPy array.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A 1D NumPy array of integers representing the transformed sequence.
    """
    # 1. Determine the length of the input array.
    n = input_grid.shape[0]

    # 2. Find the indices of the first and last non-zero elements.
    first_nz_idx, last_nz_idx = _find_first_last_nonzero_indices(input_grid)

    # 3. Handle the edge case where no non-zero integers are present.
    if first_nz_idx == -1:
        # If all zeros, return a copy of the input (or a zero array)
        return np.copy(input_grid) 

    # 4. Extract the sub-array (the "active block").
    # Slice from the first non-zero index up to and including the last non-zero index.
    active_block = input_grid[first_nz_idx : last_nz_idx + 1]

    # 5. Initialize the output_grid with zeros, same shape as input.
    output_grid = np.zeros_like(input_grid)

    # 6. Calculate the target starting index for the block in the new array.
    target_start_idx = first_nz_idx + 2
    
    # 7. Calculate the target ending index (exclusive).
    block_length = len(active_block)
    target_end_idx = target_start_idx + block_length

    # 8. Place the extracted block into the output array at the target position.
    # Ensure the placement doesn't exceed the array bounds, though examples imply it won't.
    if target_end_idx <= n:
        output_grid[target_start_idx:target_end_idx] = active_block
    # else: Handle potential out-of-bounds if needed (e.g., truncate)
    # Based on examples, this check might not be strictly necessary, but good practice.
    
    # Return the resulting output array.
    return output_grid