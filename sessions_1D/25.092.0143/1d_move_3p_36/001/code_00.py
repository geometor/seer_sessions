import numpy as np

"""
Identify the single contiguous block of non-white pixels within the input row. 
Note its color, length, and starting position. Calculate the new starting 
position of the block by adding 3 to its original starting position. 
Construct the output row, which has the same total length as the input row, 
by placing the shifted block at its new position and filling the remaining 
positions (before and after the block) with white pixels (color 0).
"""

def find_non_white_block(grid_1d):
    """
    Finds the first contiguous block of non-white pixels in a 1D grid.

    Args:
        grid_1d (np.array): A 1D numpy array representing the input row.

    Returns:
        tuple: (start_index, length, color) of the block, or None if no 
               non-white block is found.
    """
    start_index = -1
    length = 0
    color = -1
    for i, pixel in enumerate(grid_1d):
        if pixel != 0:  # Found a non-white pixel
            if start_index == -1: # Start of the block
                start_index = i
                color = pixel
            length += 1
        elif start_index != -1: # End of the block (found a white pixel after the block)
            break 
    if start_index != -1:
        return start_index, length, color
    else:
        return None # Should not happen based on task description

def transform(input_grid):
    """
    Shifts the single non-white block in a 1D input grid 3 positions to the right.

    Args:
        input_grid (list or np.array): A 1D list or numpy array representing 
                                        the input row.

    Returns:
        np.array: A 1D numpy array representing the transformed output row.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid)
    
    # Ensure it's 1D - ARC grids are often wrapped in a list
    if input_array.ndim > 1 and input_array.shape[0] == 1:
      input_array = input_array[0]
    elif input_array.ndim > 1:
        raise ValueError("Input grid must be 1-dimensional for this transformation")

    grid_length = len(input_array)

    # Find the non-white block details
    block_info = find_non_white_block(input_array)
    if block_info is None:
        # If there's no non-white block, return a copy of the input (or all white)
        # According to examples, there's always one block, but handle defensively.
        return np.zeros_like(input_array) 
        
    start_index, length, color = block_info

    # Calculate the new starting position
    new_start_index = start_index + 3

    # Initialize the output grid with the background color (white)
    output_array = np.zeros(grid_length, dtype=int) # Default is 0 (white)

    # Place the shifted block into the output grid
    # Ensure the block does not go out of bounds (though not seen in examples)
    end_placement_index = min(new_start_index + length, grid_length)
    actual_length_to_place = end_placement_index - new_start_index
    
    if new_start_index < grid_length and actual_length_to_place > 0:
        output_array[new_start_index:end_placement_index] = color

    return output_array