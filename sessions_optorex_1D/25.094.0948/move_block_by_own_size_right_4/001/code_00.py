import math
import numpy as np # Although not strictly needed for this logic, it's often useful for grid/array tasks.

def find_block(data):
    """
    Finds the first contiguous block of identical non-zero numbers in a list.

    Args:
        data: A list of numbers.

    Returns:
        A tuple containing:
        - start_index (int): The starting index of the block (-1 if not found).
        - end_index (int): The ending index of the block (-1 if not found).
        - value (int): The value of the elements in the block (0 if not found).
        - length (int): The length of the block (0 if not found).
    """
    start_index = -1
    end_index = -1
    value = 0
    in_block = False
    n = len(data)

    for i, x in enumerate(data):
        # Look for the start of a block
        if not in_block and x != 0:
            start_index = i
            value = x
            in_block = True
        # Look for the end of the block once we are in one
        elif in_block:
            # If the current element is different from the block value,
            # or if we hit a zero, the block ends at the previous element.
            if x != value:
                end_index = i - 1
                break # Found the end

    # Handle the case where the block extends to the very end of the list
    if in_block and end_index == -1:
        end_index = n - 1

    # Calculate length if a block was found
    if start_index != -1:
        length = end_index - start_index + 1
        return start_index, end_index, value, length
    else:
        # No block found
        return -1, -1, 0, 0

def transform(input_str):
    """
    Identifies a contiguous block of identical non-zero numbers in the input list
    and shifts it to the right by a distance equal to its length.

    The input is expected as a space-separated string of integers.
    The output is returned as a list of integers.
    """
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_str.split()]
    n = len(input_list)

    # Initialize the output list with zeros, same size as input
    output_list = [0] * n

    # Find the contiguous block of non-zero identical numbers
    start_index, end_index, value, length = find_block(input_list)

    # Proceed only if a valid block was found
    if start_index != -1:
        # Calculate the new starting index for the block
        # The shift amount is equal to the block's length
        shift_amount = length
        new_start_index = start_index + shift_amount

        # Copy the block elements to the new position in the output list
        # Iterate for the length of the block
        for i in range(length):
            # Calculate the index in the output list
            output_idx = new_start_index + i
            # Place the value, ensuring we don't go out of bounds
            # (though based on examples, this might not happen)
            if output_idx < n:
                output_list[output_idx] = value

    # Return the transformed list
    return output_list