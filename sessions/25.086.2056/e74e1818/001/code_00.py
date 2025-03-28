import copy
import numpy as np

"""
Identify contiguous vertical blocks of rows where each row within the block contains the same single non-white color (along with potentially white pixels). 
For each identified block, reverse the order of the rows within that block. 
Rows that are entirely white or rows that are not part of such a block remain in their original positions relative to the blocks around them.
"""

def get_row_non_white_color(row):
    """
    Finds the single non-white color in a row.
    
    Args:
        row (list): A list of integers representing a grid row.

    Returns:
        int or None: The non-white color value if exactly one is present, otherwise None.
    """
    non_white_pixels = set(pixel for pixel in row if pixel != 0)
    if len(non_white_pixels) == 1:
        return non_white_pixels.pop()
    return None # Return None if row is all white or has multiple non-white colors

def transform(input_grid):
    """
    Transforms the input grid by reversing the order of rows within contiguous blocks 
    defined by a shared single non-white color.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Initialize output_grid as a deep copy of the input to preserve original rows initially
    output_grid = copy.deepcopy(input_grid)
    height = len(input_grid)
    width = len(input_grid[0]) if height > 0 else 0
    
    processed_rows = [False] * height # Keep track of rows already part of a reversed block
    
    current_row_index = 0
    while current_row_index < height:
        # If this row was already part of a processed block, skip it
        if processed_rows[current_row_index]:
            current_row_index += 1
            continue

        # Get the non-white color of the current row
        block_color = get_row_non_white_color(input_grid[current_row_index])

        # If the row is all white or invalid (shouldn't happen based on examples), move to the next row
        if block_color is None:
            current_row_index += 1
            continue
        
        # Found a potential start of a block, find its extent
        block_start_index = current_row_index
        block_end_index = current_row_index
        
        # Look ahead to find contiguous rows with the *same* single non-white color
        next_row_index = current_row_index + 1
        while next_row_index < height:
            next_row_color = get_row_non_white_color(input_grid[next_row_index])
            if next_row_color == block_color:
                block_end_index = next_row_index
                next_row_index += 1
            else:
                # Row does not match the block color, stop extending the block
                break
        
        # If a block of size > 0 was found (it always will be at least size 1 here)
        block_rows = []
        for i in range(block_start_index, block_end_index + 1):
             block_rows.append(input_grid[i])
             processed_rows[i] = True # Mark rows as processed

        # Reverse the extracted block rows
        reversed_block = block_rows[::-1]
        
        # Place the reversed block into the output grid
        for i in range(len(reversed_block)):
            output_grid[block_start_index + i] = reversed_block[i]
            
        # Update the current_row_index to continue scanning after this block
        current_row_index = block_end_index + 1

    return output_grid
