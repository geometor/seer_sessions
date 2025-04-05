import math
import numpy as np # Including numpy for potential compatibility or future grid ops

"""
Identifies a contiguous block of a single non-zero digit within a 1D list of integers and shifts this block three positions to the left. The sequence length is maintained, and positions outside the shifted block are filled with zeros. If no non-zero block exists, the original sequence is returned.
"""

def find_non_zero_block(int_list):
    """
    Finds the first contiguous block of identical non-zero digits.

    Args:
        int_list: A list of integers.

    Returns:
        A tuple (value, start_index, end_index) if a block is found,
        otherwise None. end_index is exclusive (like Python slicing).
    """
    start_index = -1
    block_value = -1
    # Find the start of the first non-zero block
    for i, val in enumerate(int_list):
        if val != 0:
            start_index = i
            block_value = val
            break # Found the start of the block

    # If no non-zero element was found, return None
    if start_index == -1:
        return None

    # Find the end of the block (exclusive index)
    end_index = start_index
    while end_index < len(int_list) and int_list[end_index] == block_value:
        end_index += 1

    return block_value, start_index, end_index


def transform(input_sequence):
    """
    Transforms the input sequence by shifting the non-zero block left by 3 positions.

    Args:
        input_sequence: A list of integers representing the input sequence.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # Get the length of the input sequence
    n = len(input_sequence)
    if n == 0:
        return [] # Handle empty input

    # Identify the non-zero block
    block_info = find_non_zero_block(input_sequence)

    # If no non-zero block is found, return the original sequence
    if block_info is None:
        # Return a copy to avoid modifying the original if it's mutable
        return list(input_sequence) 

    # Extract block details
    block_value, start_index, end_index = block_info
    block_length = end_index - start_index

    # Calculate the new starting position for the block (shift left by 3, minimum index 0)
    new_start_index = max(0, start_index - 3)

    # Initialize the output sequence with zeros
    output_sequence = [0] * n

    # Place the block into the output sequence at the new position
    # Iterate through the length of the original block
    for i in range(block_length):
        # Calculate the target index in the output sequence
        target_index = new_start_index + i
        
        # Check if the target index is within the bounds of the output sequence
        if 0 <= target_index < n:
            # Place the block's value at the target index
            output_sequence[target_index] = block_value

    # Return the newly constructed sequence
    return output_sequence