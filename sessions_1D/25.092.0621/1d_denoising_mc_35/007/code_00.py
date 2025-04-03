"""
Identify the contiguous block of non-background (non-zero) pixels in an input grid (represented as a list or list of lists, effectively 1D). Determine the most frequent color value (dominant color) within this block. Create an output grid of the same dimensions and format where the elements corresponding to this block are all set to the identified dominant color, while the background (zero) pixels outside the block remain unchanged.
"""

import numpy as np
from collections import Counter
import math # Included for completeness, though not used in this specific logic

def transform(input_grid):
    """
    Transforms an input grid (list or list of lists) by homogenizing the 
    central non-background block with its most frequent color.

    Args:
        input_grid (list or list[list]): The input grid, effectively 1D.

    Returns:
        list or list[list]: The transformed grid in the same format as the input.
    """
    
    # Convert input list or list of lists to a numpy array
    grid_np = np.array(input_grid, dtype=int)
    
    # Store the original shape to restore it later
    original_shape = grid_np.shape
    
    # Flatten the array for easier 1D processing
    flat_grid = grid_np.flatten()
    
    # Define the background color
    background_color = 0
    
    # Find indices of all non-background (non-zero) pixels
    non_background_indices = np.where(flat_grid != background_color)[0]
    
    # If there are no non-background pixels, the grid is all background.
    # Return the original grid in its original list format.
    if len(non_background_indices) == 0:
        # No changes needed, return input in its original list structure
        return input_grid 
        
    # Identify the start and end indices of the contiguous block.
    # Assumes a single contiguous block based on examples.
    start_index = non_background_indices[0]
    end_index = non_background_indices[-1]
    
    # Extract the part of the flattened grid corresponding to the target block
    # Slice includes elements from start_index up to end_index
    target_block = flat_grid[start_index : end_index + 1]
    
    # Check if the target block is somehow empty (robustness check)
    if target_block.size == 0:
         # Should not happen if non_background_indices is not empty, but handle defensively
         return input_grid # Return original list format

    # Count the frequency of each color within the target block
    color_counts = Counter(target_block)
    
    # Find the most frequent color (dominant color).
    # most_common(1) returns [(color, count)], so get color with [0][0]
    dominant_color = color_counts.most_common(1)[0][0] 
    
    # Initialize the output flattened grid as a copy of the input flattened grid.
    output_flat_grid = flat_grid.copy()
    
    # Modify the output grid: fill the identified block range with the dominant color.
    output_flat_grid[start_index : end_index + 1] = dominant_color
    
    # Reshape the modified flattened array back to the original shape
    output_grid_np = output_flat_grid.reshape(original_shape)
    
    # Convert the final NumPy array back to a list (or list of lists) 
    # matching the original input structure and return it.
    return output_grid_np.tolist()