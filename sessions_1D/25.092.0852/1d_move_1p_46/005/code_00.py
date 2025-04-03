"""
Transformation Rule:
Identify the single contiguous block of non-white pixels within the input 1D grid.
Shift this block exactly one position to the right.
The output grid has the same dimensions as the input. The space previously occupied by the block's starting position becomes white (0), and the block occupies its new shifted position. Other white pixels remain white.
"""

import numpy as np

def find_non_white_block_info(grid_1d):
    """
    Finds the start index, end index (exclusive), and color 
    of the first contiguous non-white block in a 1D grid.

    Args:
      grid_1d: A list or 1D numpy array representing the row.

    Returns:
      A tuple (start_index, end_index, block_color). 
      Returns (None, None, None) if no non-white block is found.
    """
    grid_array = np.array(grid_1d)
    non_white_indices = np.where(grid_array != 0)[0]
    
    if len(non_white_indices) == 0:
        # No non-white pixels found at all
        return None, None, None 
    
    # Find the start of the first block
    start_index = non_white_indices[0]
    block_color = grid_array[start_index]
    
    # Find the end of this contiguous block of the *same* color
    end_index = start_index + 1
    while end_index < len(grid_array) and grid_array[end_index] == block_color:
        end_index += 1
        
    # We only care about the first block based on the examples
    # Verify contiguity just in case (though the examples only show one block)
    actual_block_indices = non_white_indices[(non_white_indices >= start_index) & (non_white_indices < end_index)]
    if len(actual_block_indices) != (end_index - start_index):
         # This indicates potential gaps or multiple blocks starting immediately,
         # but based on the task structure, we assume a single block.
         # For robustness, could add error handling or adjust logic if needed.
         pass # Assuming task guarantees a single contiguous block

    return start_index, end_index, block_color

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    Identifies a single contiguous block of non-white color and shifts it one position right.
    
    Args:
      input_grid: A list or 1D numpy array representing the input row.

    Returns:
      A numpy array representing the transformed row.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid)
    grid_size = len(input_array)

    # Initialize the output grid with the background color (white, 0)
    output_grid = np.zeros(grid_size, dtype=input_array.dtype)

    # Find the non-white block in the input
    start_index, end_index, block_color = find_non_white_block_info(input_array)

    # If a block was found, shift it
    if start_index is not None:
        # Calculate the new position for the block
        new_start_index = start_index + 1
        new_end_index = end_index + 1
        block_length = end_index - start_index

        # Ensure the new position is within the grid bounds
        # (Based on examples, the shift always fits within the grid)
        if new_end_index <= grid_size:
            # Place the block in the new position in the output grid
            output_grid[new_start_index:new_end_index] = block_color
        else:
            # Handle edge case where shift goes off the grid? 
            # The examples don't show this, so we assume it fits.
            # If needed, could truncate or handle differently.
            # For now, assume it fits based on the provided examples.
             output_grid[new_start_index:grid_size] = block_color # This would truncate if needed
             # However, sticking to example behavior, let's assume full fit.
             # Revert to the simple assignment assuming it fits:
             # output_grid[new_start_index:new_end_index] = block_color
             # Actually, the examples guarantee it fits.
             pass # No special handling needed based on examples

    # If no block was found, the output grid remains all zeros, which is correct.
    
    # Return the transformed grid as a numpy array (or convert to list if required by spec)
    # The test framework often expects lists of lists, but for 1D, a flat list or numpy array is common.
    # Let's return numpy array as it was used internally.
    return output_grid