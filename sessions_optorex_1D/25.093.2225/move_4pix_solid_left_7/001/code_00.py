import math
import numpy as np
# Add other necessary imports here if needed, though basic list operations might suffice

"""
Transforms an input sequence of 12 integers by finding a contiguous block of identical 
non-zero integers and shifting this block 4 positions to the left. The remaining 
positions in the output sequence are filled with zeros.
"""

def find_nonzero_block(sequence):
    """
    Finds the contiguous block of identical non-zero integers in the sequence.

    Args:
        sequence: A list of integers.

    Returns:
        A tuple containing:
        - value (int): The non-zero value of the block (or 0 if no block found).
        - start_index (int): The starting index of the block (-1 if no block found).
        - end_index (int): The ending index (inclusive) of the block (-1 if no block found).
        - length (int): The length of the block (0 if no block found).
    """
    start_index = -1
    end_index = -1
    value = 0
    length = 0

    for i, num in enumerate(sequence):
        # Find the start of a potential block
        if num != 0 and start_index == -1:
            start_index = i
            value = num
            end_index = i # Initialize end_index
        # If we've found the start, check if the current element continues the block
        elif start_index != -1:
            if num == value:
                end_index = i # Update end_index as the block continues
            else:
                # Block ends here (or is just one element long and the next is different/zero)
                break # Exit loop once the block ends

    if start_index != -1:
        length = end_index - start_index + 1

    return value, start_index, end_index, length


def transform(input_grid):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_grid: A list of 12 integers representing the input sequence.

    Returns:
        A list of 12 integers representing the transformed output sequence.
    """
    # 1. Identify the contiguous block of identical non-zero integers.
    block_value, block_start_index, block_end_index, block_length = find_nonzero_block(input_grid)

    # 2. Create a new output sequence of the same length, initialized with zeros.
    input_length = len(input_grid) # Typically 12 based on examples
    output_grid = [0] * input_length

    # Only proceed if a valid block was found
    if block_start_index != -1:
        # 3. Calculate the new starting index for the block.
        new_start_index = block_start_index - 4

        # 4. Place the identified block into the output sequence at the new start index.
        # Ensure the block placement stays within the bounds of the output grid.
        for i in range(block_length):
            current_output_index = new_start_index + i
            # Check if the index is valid for the output grid
            if 0 <= current_output_index < input_length:
                output_grid[current_output_index] = block_value

    return output_grid