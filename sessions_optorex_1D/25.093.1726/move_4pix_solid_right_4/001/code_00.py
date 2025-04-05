"""
Transforms an input sequence by finding a contiguous block of identical non-zero integers and shifting it 4 positions to the right, filling the original positions with zeros.
"""

import numpy as np

def find_non_zero_block(sequence):
    """
    Finds the first contiguous block of identical non-zero numbers.

    Args:
        sequence: A list or numpy array of numbers.

    Returns:
        A tuple (value, start_index, end_index) or None if no block is found.
        value: The non-zero integer value of the block.
        start_index: The starting index of the block.
        end_index: The ending index (inclusive) of the block.
    """
    start_index = -1
    block_value = 0
    for i, val in enumerate(sequence):
        if val != 0:
            if start_index == -1: # Start of a potential block
                start_index = i
                block_value = val
            elif val != block_value: # End of block because value changed
                 return block_value, start_index, i - 1
        elif start_index != -1: # End of block because zero encountered
            return block_value, start_index, i - 1

    # Handle block reaching the end of the sequence
    if start_index != -1:
        return block_value, start_index, len(sequence) - 1

    return None # No non-zero block found

def transform(input_sequence):
    """
    Shifts a contiguous block of non-zero numbers 4 positions to the right.

    Args:
        input_sequence: A list of integers representing the input.

    Returns:
        A list of integers representing the transformed output.
    """
    # Convert to numpy array for easier slicing if needed, though list operations are fine here
    input_arr = np.array(input_sequence)
    n = len(input_arr)
    
    # Initialize output_grid with zeros, same size as input
    output_sequence = [0] * n

    # Find the contiguous block of identical non-zero numbers
    block_info = find_non_zero_block(input_arr)

    if block_info:
        value, start_index, end_index = block_info
        block_length = end_index - start_index + 1
        
        # Calculate the new starting index for the block (shift right by 4)
        new_start_index = start_index + 4
        
        # Ensure the new block stays within bounds
        # (although based on examples, overflow doesn't seem to wrap around, just potentially cut off or error if not handled)
        # We will place it assuming it fits, as per examples.
        
        # Place the block into the output sequence at the new position
        for i in range(block_length):
            output_index = new_start_index + i
            # Check bounds before writing (optional based on exact task rules for overflow)
            if 0 <= output_index < n:
                output_sequence[output_index] = value
            # else: handle overflow if required, e.g., wrap around or discard

    # Return the modified output sequence (as a list)
    return output_sequence