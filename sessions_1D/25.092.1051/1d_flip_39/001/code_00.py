import numpy as np

"""
Identifies a contiguous block of non-white pixels in a 1D input array.
Within this block, it moves the first pixel (which is always magenta, color 6) 
to the end of the block, shifting the remaining pixels in the block one position 
to the left. The surrounding white pixels (color 0) remain unchanged.
"""

def find_non_white_block(grid_1d):
    """
    Finds the start and end indices of the first contiguous block of non-white pixels.

    Args:
        grid_1d: A 1D numpy array or list representing the input grid row.

    Returns:
        A tuple (start_index, end_index) or None if no non-white block is found.
        Indices are inclusive.
    """
    start_index = -1
    end_index = -1
    for i, pixel in enumerate(grid_1d):
        if pixel != 0 and start_index == -1:
            start_index = i
        if pixel != 0:
            end_index = i
        elif start_index != -1: # Found the end of the block
             break
    if start_index != -1:
        return start_index, end_index
    else:
        return None

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.

    Args:
        input_grid: A list or 1D numpy array representing the input.

    Returns:
        A list representing the transformed output.
    """
    # Ensure input is a standard list for easier manipulation
    input_list = list(input_grid)
    
    # Initialize output_grid as a copy of the input
    output_list = list(input_list)

    # Find the contiguous block of non-white pixels
    block_indices = find_non_white_block(input_list)

    if block_indices:
        start_index, end_index = block_indices
        
        # Extract the block
        block = input_list[start_index : end_index + 1]

        # Check if the block is non-empty and starts with magenta (6)
        if block and block[0] == 6:
            # Extract the magenta pixel
            magenta_pixel = block[0]
            # Extract the rest of the pixels in the block
            other_pixels = block[1:]
            
            # Construct the new block: other pixels followed by magenta
            new_block = other_pixels + [magenta_pixel]
            
            # Replace the original block segment in the output list with the new block
            output_list[start_index : end_index + 1] = new_block
            
    # Return the modified list
    return output_list
