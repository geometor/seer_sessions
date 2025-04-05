import math
import numpy as np # Although not strictly needed by the logic, might be present in the execution environment

"""
Transforms the input list by identifying a contiguous block of identical non-zero digits 
and shifting this block to the left by a number of positions equal to its length. 
The remaining positions in the output list are filled with zeros.
"""

def find_non_zero_block(input_list: list[int]) -> tuple[int, int, int]:
    """
    Finds the first contiguous block of identical non-zero numbers.

    Args:
        input_list: The list of integers to search within.

    Returns:
        A tuple containing:
        - start_index (int): The starting index of the block (-1 if no block found).
        - block_length (int): The length of the block (0 if no block found).
        - block_value (int): The value of the elements in the block (0 if no block found).
    """
    start_index = -1
    block_length = 0
    block_value = 0

    for i, val in enumerate(input_list):
        # Look for the start of a potential block (first non-zero)
        if val != 0 and start_index == -1:
            start_index = i
            block_value = val
            block_length = 1
        # If we are already in a block, check if the current element continues it
        elif start_index != -1:
            if val == block_value:
                block_length += 1
            # If the element is different (zero or another non-zero), the block ends
            else:
                break 
        # If we haven't started a block and the element is zero, continue
        # If we have finished a block (by encountering a different value), the break above handles it.
        
    # Handle case where block goes to the end of the list (loop finishes while block is active)
    if start_index != -1:
        return start_index, block_length, block_value
    else:
        # No non-zero block found
        return -1, 0, 0

def transform(input_grid: list[int]) -> list[int]:
    """
    Applies the described transformation rule to the input list.

    Args:
        input_grid: The input list of integers.

    Returns:
        A new list with the non-zero block shifted according to the rule.
    """
    list_length = len(input_grid)
    # 1. Initialize output_grid: Create a new list filled with zeros.
    output_grid = [0] * list_length

    # 2. Identify Block & 3. Record Properties: Find the non-zero block details.
    start_index, block_length, block_value = find_non_zero_block(input_grid)

    # Proceed only if a block was found. If not, the all-zero grid is returned.
    if start_index != -1:
        # 4. Calculate New Position: Determine the target start index.
        new_start_index = start_index - block_length

        # 5. Place Block: Copy the block to the new position in the output grid.
        for i in range(block_length):
            target_index = new_start_index + i
            # Ensure writing stays within list bounds [0, list_length - 1].
            if 0 <= target_index < list_length:
                output_grid[target_index] = block_value
            # Elements shifted outside bounds are implicitly handled as they are not written.

    # 6. Finalize: Return the resulting grid.
    return output_grid