"""
Identify the single contiguous block of non-white pixels (color != 0) within the input 1D grid. 
Shift this block exactly one position to the right. 
The output grid has the same dimensions as the input. The space previously occupied by the block's starting position becomes white (0), and the block occupies its new shifted position. All other pixels remain white (0).
"""

import numpy as np

def find_non_white_block_info(grid_1d):
    """
    Finds the start index, end index (exclusive), and color 
    of the first contiguous non-white block in a 1D grid.

    Args:
      grid_1d: A 1D numpy array representing the row.

    Returns:
      A tuple (start_index, end_index, block_color). 
      Returns (None, None, None) if no non-white block is found.
    """
    # Find indices of all non-white pixels
    non_white_indices = np.where(grid_1d != 0)[0]
    
    if len(non_white_indices) == 0:
        # No non-white pixels found
        return None, None, None 
    
    # The start index is the first non-white index
    start_index = non_white_indices[0]
    # Get the color of the block from the starting pixel
    block_color = grid_1d[start_index]
    
    # Find the end of this contiguous block of the *same* color
    end_index = start_index + 1
    grid_len = len(grid_1d)
    while end_index < grid_len and grid_1d[end_index] == block_color:
        end_index += 1
        
    # Assuming the task guarantees exactly one contiguous block as per examples
    return start_index, end_index, block_color

def transform(input_grid):
    """
    Applies the block shift transformation to the input grid.
    
    Args:
      input_grid: A list representing the input 1D row.

    Returns:
      A list representing the transformed 1D row.
    """
    # Convert input list to a numpy array for easier processing
    input_array = np.array(input_grid)
    grid_size = len(input_array)

    # Find the non-white block details in the input array
    start_index, end_index, block_color = find_non_white_block_info(input_array)

    # Initialize the output grid with the background color (white, 0)
    # Use the same data type as the input array to avoid potential issues
    output_array = np.zeros(grid_size, dtype=input_array.dtype)

    # Check if a non-white block was found
    if start_index is not None:
        # Calculate the new position for the block (shift right by 1)
        new_start_index = start_index + 1
        new_end_index = end_index + 1

        # Ensure the new position is valid and within the grid bounds
        # (The examples suggest the block always fits after the shift)
        if new_end_index <= grid_size:
            # Fill the segment in the output grid with the block's color
            # Assigning a scalar (block_color) to a slice automatically broadcasts it
            output_array[new_start_index:new_end_index] = block_color
        else:
            # This case is not expected based on examples, but if the block
            # went off the edge, this code would only fill up to the edge.
            # Given the examples, we assume the shift always fits.
             pass # No action needed if assumption holds

    # Convert the numpy array back to a list, as required by the ARC framework typically
    output_grid = output_array.tolist()
    
    return output_grid