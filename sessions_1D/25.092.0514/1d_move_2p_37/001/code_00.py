"""
Shift the contiguous block of non-white pixels in a single-row grid two positions to the right.
"""

import numpy as np

def find_non_white_block(row):
    """
    Finds the start index, end index (exclusive), and color of the first 
    contiguous non-white block in a row.
    Returns (start_index, end_index, color) or None if no block is found.
    """
    start_index = -1
    color = -1
    for i, pixel in enumerate(row):
        if pixel != 0: # Found the start of a non-white block
            start_index = i
            color = pixel
            break
            
    if start_index == -1: # No non-white pixels found
        return None

    end_index = start_index
    while end_index < len(row) and row[end_index] == color:
        end_index += 1
        
    return start_index, end_index, color

def transform(input_grid):
    """
    Identifies a contiguous block of non-white pixels in the input row 
    and shifts it two positions to the right in the output row.
    """
    # Input is expected to be a 1D array (or a 1xN 2D array)
    input_row = np.array(input_grid).flatten()
    height = 1
    width = len(input_row)
    
    # Initialize output_grid with the same dimensions, filled with white (0)
    output_grid = np.zeros((height, width), dtype=int)
    output_row = output_grid[0] # Work with the single row

    # Find the non-white block in the input row
    block_info = find_non_white_block(input_row)

    if block_info:
        start_index, end_index, color = block_info
        
        # Calculate the new starting position
        new_start_index = start_index + 2
        
        # Copy the block to the new position in the output row
        # Iterate through the original block's indices
        for i in range(start_index, end_index):
            # Calculate the target index in the output row
            target_index = i + 2
            # Check if the target index is within the bounds of the output row
            if 0 <= target_index < width:
                output_row[target_index] = color
                
    # Return the modified grid (reshaped back if necessary, although for 1xN it doesn't change much)
    # Ensure it's returned as a list of lists or similar expected format if needed,
    # but numpy array is usually fine for ARC tasks.
    # If the input was guaranteed 2D (1xN), reshape: return output_grid.tolist()
    # If input could be 1D, this is fine: return output_grid 
    # Based on example format, returning 2D list of lists is safer.
    return output_grid.tolist()
