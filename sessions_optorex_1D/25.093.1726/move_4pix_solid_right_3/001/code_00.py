import math
import collections

"""
Identifies a contiguous block of identical non-zero integers in a 12-element list.
Shifts this block exactly 4 positions to the right.
The original position of the block is replaced with zeros.
The output is a new 12-element list reflecting this shift.
"""

def find_block(input_list):
    """
    Finds the first contiguous block of identical non-zero numbers.

    Args:
        input_list: A list of integers.

    Returns:
        A tuple (value, start_index, end_index) representing the block's
        value, starting index (inclusive), and ending index (exclusive).
        Returns (None, -1, -1) if no such block is found.
    """
    start_index = -1
    end_index = -1
    value = None
    n = len(input_list)

    for i in range(n):
        # If we find a non-zero element and haven't started a block yet
        if input_list[i] != 0 and start_index == -1:
            start_index = i
            value = input_list[i]
        # If we have started a block and find a zero or a different non-zero number
        elif start_index != -1 and (input_list[i] == 0 or input_list[i] != value):
            end_index = i
            break # Block ended

    # If a block was started but didn't end before the list finished
    if start_index != -1 and end_index == -1:
        end_index = n

    return value, start_index, end_index

def transform(input_list):
    """
    Transforms the input list by shifting the non-zero block 4 positions right.

    Args:
        input_list: A list of 12 integers containing one non-zero block.

    Returns:
        A new list of 12 integers with the block shifted.
    """
    # Define constants based on observed pattern
    sequence_length = 12
    shift_distance = 4

    # Initialize the output list with zeros
    output_list = [0] * sequence_length

    # 1. Identify the contiguous block of identical non-zero integers
    block_value, start_index, end_index = find_block(input_list)

    # Check if a valid block was found
    if block_value is None or start_index == -1:
        # Should not happen based on problem description, but good practice
        return output_list # Return the list of zeros

    # 2. Calculate the new position for the block
    new_start_index = start_index + shift_distance
    new_end_index = end_index + shift_distance

    # 3. Place the block into the output list at the new position
    # Ensure the new indices are within the bounds of the list
    # (Assumed valid based on examples, but checking prevents errors)
    actual_start = max(0, new_start_index)
    actual_end = min(sequence_length, new_end_index)

    for i in range(actual_start, actual_end):
         # Calculate the corresponding index within the original block length
         # This isn't strictly needed here since we know the value,
         # but useful if block contents varied within the block.
         # original_block_index = i - new_start_index
         # output_list[i] = input_list[start_index + original_block_index]
         # Simpler: just use the constant block value
         output_list[i] = block_value


    # 4. Return the modified output sequence
    return output_list
