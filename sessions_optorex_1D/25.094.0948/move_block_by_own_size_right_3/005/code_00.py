"""
Transformation Rule:
Identify the single contiguous block of identical non-zero digits in the input sequence (1D list). 
Shift this block to the right by a distance equal to its own length. 
The output sequence has the same length as the input, with the shifted block placed in its new position and all other elements set to zero.
"""

import numpy as np # Although not strictly necessary for list operations, numpy might be assumed by the environment or useful for potential generalizations.

def _find_block(sequence):
    """
    Helper function to find the first contiguous block of identical non-zero digits.

    Args:
        sequence: A list of integers.

    Returns:
        A tuple (value, start_index, length) representing the block's digit,
        its starting index, and its length. Returns (None, -1, 0) if no 
        such block is found or if the input is empty.
    """
    if not sequence: # Handle empty sequence case
        return None, -1, 0
        
    value = None
    start_index = -1
    length = 0
    in_block = False

    # Iterate through the sequence to find the start and extent of the block
    for i, digit in enumerate(sequence):
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
            # Found the end of the block, return its details
            # Based on the problem description, we assume only one block exists.
            return value, start_index, length

    # If we finished iterating and were still in a block (block ends at the sequence end)
    if in_block:
        return value, start_index, length
        
    # If the loop finishes without ever starting a block
    return None, -1, 0

def transform(input_grid):
    """
    Applies the transformation rule to the input sequence (grid).

    Identifies a contiguous block of identical non-zero digits and shifts 
    it to the right by a distance equal to the block's length.

    Args:
        input_grid: A list of integers representing the input sequence.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # Ensure input is treated as a list for consistency, though numpy array input might also work with _find_block
    input_sequence = list(input_grid) 
    
    # Determine the size of the grid
    grid_size = len(input_sequence)
    
    # Initialize the output grid with zeros, same size as input
    output_grid = [0] * grid_size

    # Find the non-zero block in the input sequence
    block_value, block_start_index, block_length = _find_block(input_sequence)

    # Proceed only if a valid block was found
    if block_value is not None and block_length > 0:
        # Calculate the new starting position for the block
        # The shift distance is equal to the block's length
        new_start_index = block_start_index + block_length

        # Place the block into the output grid at the new position
        # Iterate for the length of the block
        for i in range(block_length):
            # Calculate the index in the output grid where the current part of the block should be placed
            target_index = new_start_index + i
            
            # Ensure the target index is within the bounds of the grid
            if target_index < grid_size:
                output_grid[target_index] = block_value
            else:
                # If the target index goes beyond the grid size, stop placing digits.
                # This handles cases where the shift pushes the block partially or fully off the grid.
                break 

    # Return the newly constructed grid with the shifted block
    return output_grid