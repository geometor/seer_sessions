"""
Transformation Rule:
Identify the single contiguous block of identical non-zero digits in the input sequence (1D array/list). 
Shift this block to the right by a distance equal to its own length. 
The output sequence has the same length as the input, with the shifted block placed in its new position and all other elements set to zero.
"""

import numpy as np

def _find_block(sequence):
    """
    Helper function to find the first contiguous block of identical non-zero digits.

    Args:
        sequence: A NumPy array or list of integers.

    Returns:
        A tuple (value, start_index, length) representing the block's digit,
        its starting index, and its length. Returns (None, -1, 0) if no 
        such block is found or if the input is empty.
    """
    if len(sequence) == 0:
        return None, -1, 0
        
    value = None
    start_index = -1
    length = 0
    in_block = False

    # Iterate through the sequence to find the start and extent of the block
    for i, digit in enumerate(sequence):
        # Ensure comparison works correctly (needed for NumPy types)
        is_non_zero = (digit != 0) 
        
        # Found the start of a potential block
        if not in_block and is_non_zero:
            value = digit
            start_index = i
            length = 1
            in_block = True
        # Continue counting if inside the block and the digit matches
        elif in_block and digit == value:
            length += 1
        # Stop counting if inside a block but the digit doesn't match or is zero
        elif in_block and (digit != value or not is_non_zero):
            break # Found the end of the block, exit loop

    # If we iterated through the whole sequence but never started a block
    if not in_block:
        return None, -1, 0
        
    return value, start_index, length

def transform(input_grid):
    """
    Applies the transformation rule to the input sequence (grid).

    Identifies a contiguous block of identical non-zero digits and shifts 
    it to the right by a distance equal to the block's length.

    Args:
        input_grid: A NumPy array representing the input sequence. 
                    (Assumed based on previous errors, robust to lists too).

    Returns:
        A NumPy array representing the transformed sequence.
    """
    # Ensure input is a NumPy array for consistent handling
    input_array = np.array(input_grid)
    
    # Determine the size of the grid
    grid_size = len(input_array)
    
    # Initialize the output grid with zeros, same size and type as input might imply
    # Using int type explicitly assuming integer digits
    output_grid = np.zeros(grid_size, dtype=int) 

    # Find the non-zero block in the input sequence
    block_value, block_start_index, block_length = _find_block(input_array)

    # Proceed only if a valid block was found
    if block_value is not None and block_length > 0:
        # Calculate the new starting position for the block
        # The shift distance is equal to the block's length
        new_start_index = block_start_index + block_length

        # Calculate the end index for slicing, ensuring it doesn't exceed grid bounds
        new_end_index = min(new_start_index + block_length, grid_size)

        # Place the block into the output grid at the new position using slicing
        # Check if the new start index is valid and there's space to place the block
        if new_start_index < grid_size:
             # Determine how many elements of the block actually fit
             num_elements_to_place = new_end_index - new_start_index
             if num_elements_to_place > 0:
                 output_grid[new_start_index:new_end_index] = block_value

    # Return the newly constructed grid with the shifted block
    return output_grid