"""
Transforms the input grid by identifying the single contiguous horizontal block
of non-white pixels and shifting it two positions to the right. The grid size
and the block's color and length remain unchanged. The background is white (0).
"""

import numpy as np

def find_block_1d(row):
    """
    Finds the first contiguous block of non-zero pixels in a 1D list.

    Args:
        row: A list of integers representing a row of the grid.

    Returns:
        A tuple containing:
        - color (int): The color of the block (non-zero).
        - start_index (int): The starting index of the block.
        - length (int): The length of the block.
        Returns None if no non-zero block is found.
    """
    start_index = -1
    block_color = 0
    length = 0
    for i, pixel in enumerate(row):
        if pixel != 0:
            if start_index == -1:
                start_index = i
                block_color = pixel
                length = 1
            elif pixel == block_color:
                length += 1
            else: # Found a different color, block ended
                break
        elif start_index != -1: # Found a zero after the block started
            break
            
    if start_index != -1:
        return block_color, start_index, length
    else:
        return None

def transform(input_grid_str):
    """
    Shifts the non-white horizontal block in the input grid two positions to the right.

    Args:
        input_grid_str: A string representing the 1D input grid, with integers
                         separated by spaces.

    Returns:
        A string representing the transformed 1D output grid, with integers
        separated by spaces. Returns the original string if no block is found.
    """
    # Parse the input string into a list of integers
    input_row = [int(p) for p in input_grid_str.split()]
    grid_length = len(input_row)

    # Find the non-white block
    block_info = find_block_1d(input_row)

    if block_info is None:
        # If no block is found, return the original grid string
        # Although the problem description implies a block always exists.
        return input_grid_str

    block_color, start_index, length = block_info

    # Initialize the output grid with white pixels (0)
    output_row = [0] * grid_length

    # Calculate the new starting position
    new_start_index = start_index + 2

    # Check boundaries (although not strictly needed based on examples)
    if new_start_index + length <= grid_length:
        # Place the block in the new position in the output grid
        for i in range(length):
            output_row[new_start_index + i] = block_color
    else:
        # Handle case where the block shifts partially or fully off-grid
        # Based on examples, this doesn't happen, but for robustness:
        # Copy only the part that fits.
        print(f"Warning: Block shift exceeds grid boundary. Original start={start_index}, length={length}, grid_length={grid_length}")
        for i in range(length):
            target_index = new_start_index + i
            if 0 <= target_index < grid_length:
                 output_row[target_index] = block_color
        # If the problem strictly guarantees the shift fits, this else block
        # can be removed and the boundary check above is also optional.

    # Format the output list back into a space-separated string
    output_grid_str = " ".join(map(str, output_row))

    return output_grid_str