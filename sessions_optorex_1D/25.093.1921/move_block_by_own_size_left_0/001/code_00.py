import math
from typing import List, Tuple, Optional

"""
Identifies a contiguous block of identical non-zero digits in a 1D input sequence.
Shifts this block leftwards by an amount equal to its length.
The rest of the sequence is filled with zeros.

Example:
Input:  [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0] (Block '1 1 1', length 3, starts at index 3)
Shift amount = 3
New start index = 3 - 3 = 0
Output: [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]

Input:  [0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0] (Block '4 4 4', length 3, starts at index 5)
Shift amount = 3
New start index = 5 - 3 = 2
Output: [0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0]
"""

def find_block(sequence: List[int]) -> Optional[Tuple[int, int, int]]:
    """
    Finds the first contiguous block of identical non-zero digits.

    Args:
        sequence: The input list of integers.

    Returns:
        A tuple containing (block_value, start_index, block_length),
        or None if no such block is found.
    """
    start_index = -1
    block_value = 0
    block_length = 0

    for i, val in enumerate(sequence):
        if val != 0:
            # Start of a potential block
            if start_index == -1:
                start_index = i
                block_value = val
                block_length = 1
            # Continue the current block if value matches
            elif val == block_value:
                block_length += 1
            # End of the block (different non-zero value or zero encountered)
            else:
                # Found the block, stop searching
                break
        elif start_index != -1:
            # End of the block (zero encountered after block started)
            break

    if start_index != -1:
        return block_value, start_index, block_length
    else:
        # Should not happen based on task description, but handle defensively
        return None

def transform(input_grid: List[int]) -> List[int]:
    """
    Transforms the input sequence by finding a non-zero block and shifting it left
    by its length.

    Args:
        input_grid: The input list of integers.

    Returns:
        The transformed list of integers.
    """
    # Find the non-zero block details
    block_info = find_block(input_grid)

    # Initialize the output grid with zeros, same length as input
    output_grid = [0] * len(input_grid)

    # If a block was found, calculate its new position and place it
    if block_info:
        block_value, start_index, block_length = block_info

        # Calculate the shift amount (equal to block length)
        shift_amount = block_length

        # Calculate the new starting index for the block
        new_start_index = start_index - shift_amount

        # Place the block in the output grid at the new position
        # Ensure indices stay within the bounds of the output grid
        for i in range(block_length):
            target_index = new_start_index + i
            # Only place if the index is valid
            if 0 <= target_index < len(output_grid):
                output_grid[target_index] = block_value
            # else: the element is shifted off the grid (implicitly handled by init to 0)

    # Return the transformed grid
    return output_grid
