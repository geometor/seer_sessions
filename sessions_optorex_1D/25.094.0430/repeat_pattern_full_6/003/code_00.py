"""
Transforms an input NumPy array by identifying a repeating sequence (Pattern_S) 
at the beginning, which appears twice consecutively followed by zeros. It then 
generates the output array by tiling (repeating) Pattern_S cyclically until 
the original length of the input array is reached.
"""

import numpy as np
import math

def find_first_zero_index(arr):
  """Finds the index of the first zero in a NumPy array."""
  zero_indices = np.where(arr == 0)[0]
  if len(zero_indices) > 0:
    return zero_indices[0]
  else:
    # Handle case where no zeros are found, though examples suggest they exist.
    # If no zeros, the pattern might fill the whole array if length is even.
    # This case needs clarification if it occurs, but based on examples,
    # we assume zeros are always present as padding.
    return len(arr) # Treat as if zeros start after the last element


def tile_pattern(pattern, target_length):
  """Repeats (tiles) a pattern until it reaches the target length."""
  pattern_len = len(pattern)
  if pattern_len == 0:
      # Avoid division by zero if pattern is empty (shouldn't happen with valid inputs)
      return np.array([])
  
  num_repeats = math.ceil(target_length / pattern_len)
  tiled_array = np.tile(pattern, num_repeats)
  
  # Truncate to the exact target length
  return tiled_array[:target_length]


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Identifies a repeating pattern at the start of the input array (format P|P|0s)
    and generates an output array by tiling the pattern P to the original length.
    
    Args:
        input_grid: A 1D NumPy array of integers.
        
    Returns:
        A 1D NumPy array representing the transformed output.
    """
    
    # Get the total length of the input array
    total_length = len(input_grid)
    
    # Find the index of the first zero, marking the end of the P|P block
    first_zero_idx = find_first_zero_index(input_grid)
    
    # Calculate the length of the fundamental pattern (P)
    # We assume first_zero_idx is > 0 and even based on examples.
    # Integer division ensures L is an integer.
    pattern_length = first_zero_idx // 2
    
    # Extract the fundamental pattern (P) from the start of the input
    pattern_s = input_grid[:pattern_length]
    
    # Generate the output array by tiling the pattern P to the total length
    output_grid = tile_pattern(pattern_s, total_length)
    
    return output_grid
