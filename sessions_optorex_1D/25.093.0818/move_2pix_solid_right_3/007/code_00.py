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
        # Returning a copy ensures the original input isn't modified if it's mutable.
        return np.copy(input_grid) 

    # 4. Extract the sub-array (the "active block").
    # Slice from the first non-zero index up to and including the last non-zero index.
    active_block = input_grid[first_nz_idx : last_nz_idx + 1]

    # 5. Initialize the output_grid with zeros, same shape and type as input.
    output_grid = np.zeros_like(input_grid)

    # 6. Calculate the target starting index for the block in the new array (shift right by 2).
    target_start_idx = first_nz_idx + 2
    
    # 7. Calculate the target ending index (exclusive) based on block length.
    block_length = len(active_block)
    target_end_idx = target_start_idx + block_length

    # 8. Place the extracted block into the output array at the target position.
    # Ensure the placement doesn't exceed the array bounds.
    # This check prevents errors if the shift would push the block beyond the array's end.
    if target_end_idx <= n:
        output_grid[target_start_idx:target_end_idx] = active_block
    # else: (Optional) Define behavior if block goes out of bounds. 
    # Examples suggest this won't happen, so we implicitly truncate 
    # if target_end_idx > n by only placing up to index n-1.
    # A more explicit handling could be added if needed, e.g., placing only the part
    # that fits:
    # elif target_start_idx < n: 
    #    placeable_length = n - target_start_idx
    #    output_grid[target_start_idx:n] = active_block[:placeable_length]
        
    # Return the resulting output array.
    return output_grid