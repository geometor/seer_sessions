import numpy as np
from typing import List

"""
Identifies a single contiguous block of non-white pixels in the input row, 
shifts this block two positions to the right, and places it in an otherwise 
white output row of the same dimensions.
"""

def find_non_white_block(input_row: List[int]):
    """
    Finds the first contiguous block of non-white pixels.

    Args:
        input_row: The input list representing the row.

    Returns:
        A tuple (color, start_index, length) if a block is found,
        otherwise None.
    """
    start_index = -1
    color = -1
    length = 0

    for i, pixel in enumerate(input_row):
        if pixel != 0:  # Found a non-white pixel
            if start_index == -1:  # Start of a new block
                start_index = i
                color = pixel
                length = 1
            elif pixel == color: # Continuation of the current block
                 length += 1
            else: # Found a different color - stop (assuming only one block)
                 break
        elif start_index != -1: # Found white after a block started
            # Block ended
            break # Assuming only one block needs to be found

    if start_index != -1:
        return color, start_index, length
    else:
        return None

def transform(input_grid: List[int]) -> List[int]:
    """
    Transforms the input row by shifting the non-white block right by 2 positions.

    Args:
        input_grid: A list of integers representing the input row.

    Returns:
        A list of integers representing the transformed output row.
    """
    # Find the non-white block in the input row
    block_info = find_non_white_block(input_grid)

    # Initialize the output grid with white pixels (0)
    # Use the same length as the input grid
    output_grid = [0] * len(input_grid)

    if block_info:
        color, start_index, length = block_info

        # Calculate the new starting position (shifted right by 2)
        new_start_index = start_index + 2

        # Place the block in the output grid at the new position
        # Ensure the block doesn't go out of bounds
        for i in range(length):
            target_index = new_start_index + i
            if target_index < len(output_grid):
                output_grid[target_index] = color
            else:
                # Stop if the block goes past the end of the grid
                break

    return output_grid
