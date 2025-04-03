"""
Transforms a 1D grid (represented as a 1xN list of lists) by replacing contiguous 
horizontal blocks of magenta (6) pixels with a new color based on the block's length:
- Blocks of length 1 become red (2).
- Blocks of length 2 become gray (5).
- Blocks of length 3 become azure (8).
White (0) pixels remain unchanged in their original positions. Assumes input contains
only white (0) and magenta (6).
"""

import numpy as np

def find_contiguous_blocks(row_array, target_color):
    """
    Finds contiguous blocks of a target color in a 1D numpy array.
    Yields tuples of (start_index, length).
    """
    width = len(row_array)
    i = 0
    while i < width:
        if row_array[i] == target_color:
            block_start = i
            block_length = 0
            # Scan forward to find the end of the block
            while i < width and row_array[i] == target_color:
                block_length += 1
                i += 1
            yield (block_start, block_length)
        else:
            # Not the target color, move to the next pixel
            i += 1

def get_replacement_color(block_length):
    """
    Determines the replacement color based on the block length.
    Returns None if the length doesn't match a defined rule (1, 2, or 3).
    """
    if block_length == 1:
        return 2 # Red
    elif block_length == 2:
        return 5 # Gray
    elif block_length == 3:
        return 8 # Azure
    else:
        # No rule defined for other lengths based on examples
        return None 

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Validate input format and handle empty grid case
    if not input_grid or not isinstance(input_grid, list) or not input_grid[0] or not isinstance(input_grid[0], list):
        # Return empty list or handle error as appropriate for the environment
        # Returning input might be safer if format is unexpected but non-empty
        return input_grid 
        
    # Extract the single row from the input grid representation
    input_row_list = input_grid[0]
    
    # Convert to numpy array for efficient processing
    input_array = np.array(input_row_list, dtype=int)
    
    # Initialize the output array as a copy of the input array.
    # White pixels (0) are already correctly placed.
    output_array = input_array.copy()
    
    # Find all contiguous blocks of magenta (6)
    magenta_color = 6
    for block_start, block_length in find_contiguous_blocks(input_array, magenta_color):
        # Determine the replacement color based on block length
        replacement_color = get_replacement_color(block_length)
        
        # If a valid replacement color exists, update the output array
        if replacement_color is not None:
            output_array[block_start : block_start + block_length] = replacement_color
            
    # Convert the modified numpy array back to the required list-of-lists format
    output_grid = [output_array.tolist()]
    
    return output_grid