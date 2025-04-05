import numpy as np
import math

"""
Identify the contiguous segment of the input sequence (length 12) starting from 
the index of the first non-zero integer and ending at the index of the last 
non-zero integer. Shift this entire segment exactly 4 positions to the right 
within a new sequence of the same shape and dtype, filling the remaining 
positions with zeros. If the input sequence contains only zeros, the output is 
identical to the input. The input is assumed to represent a 1D sequence, 
potentially provided as a 1D NumPy array or a structure flattenable to 1D.
"""

def find_non_zero_bounds(data_array_1d):
  """
  Finds the indices of the first and last non-zero elements in a 1D NumPy array.

  Args:
    data_array_1d: The 1D NumPy array to search.

  Returns:
    A tuple (first_idx, last_idx). Returns (None, None) if no non-zero 
    elements are found.
  """
  # Find indices of all non-zero elements
  non_zero_indices = np.nonzero(data_array_1d)[0] 
  
  # Check if any non-zero elements were found
  if non_zero_indices.size == 0:
    return None, None
    
  # The first index in the tuple is the first non-zero index
  first_idx = non_zero_indices[0]
  # The last index in the tuple is the last non-zero index
  last_idx = non_zero_indices[-1]
  
  return first_idx, last_idx

def transform(input_grid):
    """
    Transforms the input grid by shifting the core non-zero segment 
    4 positions to the right.

    Args:
      input_grid: A NumPy array representing the sequence (potentially 1xN, Nx1, or 1D).

    Returns:
      A new NumPy array of the same shape and dtype with the segment shifted.
    """
    
    # Ensure we are working with a 1D representation for easier indexing
    # Flatten works for 1D, 1xN, Nx1 arrays
    input_array_1d = input_grid.flatten()
    
    # Define constants from the observed pattern
    array_length = input_array_1d.shape[0] # Get length from the flattened array
    if array_length == 0: # Handle empty input case
        return np.copy(input_grid) # Return a copy of the original shape

    # Expecting length 12 based on examples, but use actual length for robustness
    expected_length = 12 
    # The shift amount is constant based on examples
    shift_amount = 4 

    # Find the boundaries of the non-zero segment in the 1D array
    first_nz_idx, last_nz_idx = find_non_zero_bounds(input_array_1d)

    # Handle the case where the array is all zeros
    if first_nz_idx is None:
      # If no non-zeros, return a copy of the original input grid
      return np.copy(input_grid) 

    # Extract the segment from the 1D array
    # The segment includes all elements from the first non-zero to the last non-zero
    segment = input_array_1d[first_nz_idx : last_nz_idx + 1]

    # Calculate the new starting position for the segment
    new_start_idx = first_nz_idx + shift_amount

    # Initialize the output array (1D) with zeros, preserving the data type
    output_array_1d = np.zeros(array_length, dtype=input_grid.dtype)

    # Place the segment into the 1D output array at the new position
    segment_len = segment.shape[0] # Length of the segment
    new_end_idx = new_start_idx + segment_len # Calculate potential end index
    
    # Check bounds before placing to avoid errors if segment shifted off the end
    # (though examples suggest it always fits within length 12)
    if new_end_idx <= array_length:
        output_array_1d[new_start_idx : new_end_idx] = segment
    else:
        # If the segment goes out of bounds, truncate it
        fit_len = array_length - new_start_idx
        if fit_len > 0: # Ensure there's space to place at least part of the segment
             output_array_1d[new_start_idx : array_length] = segment[:fit_len] 
        # If fit_len <= 0, the start index is already out of bounds, segment is not placed.

    # Reshape the 1D output array back to the original input grid shape
    output_grid = output_array_1d.reshape(input_grid.shape)

    return output_grid