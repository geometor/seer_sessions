import numpy as np
import copy

"""
Identify the contiguous horizontal block of non-white pixels in the input row.
Shift this block one position to the right. The space vacated by the block 
becomes white. The grid dimensions and the block's color and size remain unchanged.
"""

def find_non_white_block(row):
    """
    Finds the start and end indices and the color of the first 
    contiguous non-white block in a row.
    
    Args:
        row (list): A list representing a row of the grid.

    Returns:
        tuple: (start_index, end_index, color) or None if no block found.
    """
    start_index = -1
    end_index = -1
    color = 0
    in_block = False
    for i, pixel in enumerate(row):
        if pixel != 0 and not in_block:
            start_index = i
            color = pixel
            in_block = True
        elif pixel == 0 and in_block:
            end_index = i - 1
            break
        elif i == len(row) - 1 and in_block: # Handle block ending at the edge
             end_index = i

    if start_index != -1 and end_index != -1:
        return start_index, end_index, color
    else:
        # Check if the entire row is the block
        if all(p != 0 for p in row) and len(row) > 0:
             return 0, len(row) - 1, row[0]
        return None

def transform(input_grid):
    """
    Shifts the single contiguous non-white block in a 1xN grid one position to the right.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid (1 row).

    Returns:
        list[list[int]]: A 2D list representing the transformed grid.
    """
    # Ensure it's a 1xN grid
    if len(input_grid) != 1:
        # Handle error or unexpected input format if necessary
        # For now, assume valid input based on examples
        pass 
        
    input_row = input_grid[0]
    height = 1
    width = len(input_row)
    
    # Initialize output_grid with the same dimensions, filled with white (0)
    output_grid = [[0 for _ in range(width)] for _ in range(height)]
    output_row = output_grid[0]

    # Find the non-white block in the input row
    block_info = find_non_white_block(input_row)

    if block_info:
        start_index, end_index, color = block_info
        block_length = end_index - start_index + 1
        
        # Calculate the new starting position (shifted right by 1)
        new_start_index = start_index + 1
        
        # Check bounds (although examples don't hit the boundary)
        if new_start_index + block_length <= width:
            # Copy the block to the new position in the output row
            for i in range(block_length):
                output_row[new_start_index + i] = color
        else:
            # Handle case where shift goes out of bounds if needed
            # Based on examples, this doesn't happen, so we copy as calculated
             for i in range(block_length):
                 if new_start_index + i < width:
                    output_row[new_start_index + i] = color


    # If no block found, the output is just the initialized white grid
    
    return output_grid