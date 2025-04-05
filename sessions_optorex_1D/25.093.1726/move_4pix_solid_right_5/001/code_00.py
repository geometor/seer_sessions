import numpy as np
from typing import List

"""
Identifies a contiguous block of identical non-zero digits in the input list, 
determines its start index, length, and digit value. Creates a new list of 
the same size initialized with zeros. Calculates the new start index by adding 
4 to the original start index. Places the identified block into the new list 
at the calculated new start index.
"""

def find_contiguous_block(data: List[int]):
    """
    Finds the first contiguous block of identical non-zero digits.

    Args:
        data: The input list of integers.

    Returns:
        A tuple containing (start_index, length, value) of the block,
        or (None, 0, None) if no such block is found.
    """
    start_index = None
    length = 0
    value = None
    in_block = False

    for i, digit in enumerate(data):
        if not in_block and digit != 0:
            # Start of a potential block
            start_index = i
            value = digit
            length = 1
            in_block = True
        elif in_block:
            if digit == value:
                # Continue the block
                length += 1
            else:
                # End of the block
                return start_index, length, value
    
    # Handle case where block goes to the end of the list
    if in_block:
        return start_index, length, value

    # No block found
    return None, 0, None

def transform(input_list: List[int]) -> List[int]:
    """
    Shifts a contiguous block of identical non-zero digits 4 positions to the right.

    Args:
        input_list: A list of 12 integers containing zeros and one contiguous block
                   of identical non-zero digits.

    Returns:
        A new list of 12 integers where the block has been shifted 4 positions
        to the right, and other positions are filled with zeros.
    """
    list_length = len(input_list)
    # Initialize output_list with zeros
    output_list = [0] * list_length

    # Find the contiguous block in the input list
    start_index, length, value = find_contiguous_block(input_list)

    # If a block was found
    if start_index is not None:
        # Calculate the new starting index for the block
        new_start_index = start_index + 4

        # Place the block into the output list at the new position
        # Ensure the placement does not go out of bounds (though examples don't show this)
        for i in range(length):
            target_index = new_start_index + i
            if 0 <= target_index < list_length:
                output_list[target_index] = value

    return output_list
