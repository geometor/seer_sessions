import math
import numpy as np # Although not strictly necessary for this list logic, it's often useful.

"""
Identify the contiguous block of identical non-zero numbers in the input list.
If the block starts at an index greater than 0, shift the block one position to the left
by removing the zero immediately preceding it and appending a zero to the end of the list.
If the block starts at index 0 or no non-zero block is found, return the list unchanged.
"""

def find_non_zero_block(data):
    """
    Finds the start index, end index (exclusive), and value of the first
    contiguous block of identical non-zero numbers.

    Args:
        data: A list of numbers.

    Returns:
        A tuple (start_index, end_index, value) if a block is found,
        otherwise returns (None, None, None).
    """
    start_index = -1
    block_value = None
    for i, val in enumerate(data):
        if val != 0:
            if start_index == -1: # Start of a potential block
                start_index = i
                block_value = val
            elif val != block_value: # Found a different non-zero, previous block ended
                 # This case shouldn't happen based on examples, but good to consider
                 # For this problem, we assume only one block type exists.
                 # If we hit a different non-zero, the block assumption is violated.
                 # Let's stick to finding the *first* block.
                 end_index = i
                 return start_index, end_index, block_value
        elif start_index != -1: # We were in a block, and hit a zero, so the block ended
            end_index = i
            return start_index, end_index, block_value

    # Handle case where block goes to the end of the list
    if start_index != -1:
        end_index = len(data)
        return start_index, end_index, block_value

    # No non-zero block found
    return None, None, None


def transform(input_list):
    """
    Transforms the input list by shifting the non-zero block one step left.

    Args:
        input_list: The input list of integers.

    Returns:
        A new list with the non-zero block shifted left, or a copy of the
        input list if no shift is possible/needed.
    """
    # Find the non-zero block
    start_index, end_index, _ = find_non_zero_block(input_list)

    # Check if a block was found and if it's not already at the beginning
    if start_index is not None and start_index > 0:
        # Create the output list by manipulating slices
        # 1. Part before the zero preceding the block
        part1 = input_list[:start_index - 1]
        # 2. The block itself
        block = input_list[start_index:end_index]
        # 3. Part after the block
        part3 = input_list[end_index:]
        # 4. The new zero to append
        padding_zero = [0]

        # Concatenate parts to form the new list
        output_list = part1 + block + part3 + padding_zero
        return output_list
    else:
        # If no block found or block starts at index 0, return a copy
        output_list = list(input_list) # Return a copy to avoid modifying original if it's mutable elsewhere
        return output_list
