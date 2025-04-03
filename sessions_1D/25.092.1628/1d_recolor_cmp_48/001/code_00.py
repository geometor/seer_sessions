"""
Identifies all contiguous horizontal blocks of red (2) pixels in the input row.
Finds the maximum length among these red blocks.
Changes the color of all red blocks that have this maximum length to blue (1).
Leaves all other pixels unchanged.
"""

import numpy as np

def find_blocks(grid_row, target_color):
    """
    Finds contiguous blocks of a specific color in a 1D row.

    Args:
        grid_row (np.array): The input row (1D numpy array).
        target_color (int): The color value to search for blocks of.

    Returns:
        list: A list of tuples, where each tuple represents a block:
              (start_index, end_index, length).
    """
    blocks = []
    in_block = False
    start_index = -1
    for i, pixel in enumerate(grid_row):
        if pixel == target_color and not in_block:
            # Start of a new block
            in_block = True
            start_index = i
        elif pixel != target_color and in_block:
            # End of the current block
            in_block = False
            end_index = i - 1
            length = end_index - start_index + 1
            blocks.append((start_index, end_index, length))
        # Handle case where the block ends at the last pixel
        if pixel == target_color and in_block and i == len(grid_row) - 1:
            end_index = i
            length = end_index - start_index + 1
            blocks.append((start_index, end_index, length))
            
    return blocks

def transform(input_grid):
    """
    Transforms the input grid according to the rule: change the longest
    contiguous block(s) of red (2) pixels to blue (1).

    Args:
        input_grid (list or np.array): A 1D list or numpy array representing the input row.

    Returns:
        np.array: The transformed 1D numpy array.
    """
    # Ensure input is a numpy array for easier manipulation
    input_row = np.array(input_grid)
    
    # Initialize output_grid as a copy of the input
    output_grid = input_row.copy()

    # Find all contiguous blocks of red (2) pixels
    red_blocks = find_blocks(input_row, 2)

    # If no red blocks are found, return the original grid
    if not red_blocks:
        return output_grid

    # Find the maximum length among the red blocks
    max_length = 0
    for start, end, length in red_blocks:
        if length > max_length:
            max_length = length

    # Identify all blocks that have the maximum length
    longest_blocks = []
    for start, end, length in red_blocks:
        if length == max_length:
            longest_blocks.append((start, end, length))

    # Change the color of the pixels in the longest blocks from red (2) to blue (1)
    for start, end, length in longest_blocks:
        # Slicing includes start but excludes end+1, hence end+1
        output_grid[start : end + 1] = 1 

    return output_grid
