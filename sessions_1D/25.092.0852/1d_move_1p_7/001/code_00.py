import numpy as np
from typing import List, Tuple

"""
Identify the single contiguous block of non-background (non-white) colored pixels 
in the input row. Shift this block one position horizontally to the right. 
Fill the vacated space with the background color (white, 0). The grid size 
remains unchanged.
"""

def find_contiguous_block(row: List[int], background_color: int = 0) -> Tuple[int, int, int]:
    """
    Finds the start index, end index, and color of the first contiguous 
    block of non-background color in a 1D list.

    Args:
        row: The input list (row of the grid).
        background_color: The integer value representing the background color.

    Returns:
        A tuple containing (start_index, end_index, color) of the block.
        Returns (-1, -1, -1) if no such block is found.
    """
    start_index = -1
    end_index = -1
    block_color = -1
    
    for i, pixel in enumerate(row):
        if pixel != background_color:
            if start_index == -1:
                start_index = i
                block_color = pixel
            # Continue extending the block if the color matches
            if start_index != -1 and pixel == block_color:
                 end_index = i
            # If a different non-background color is found, stop (assuming only one block)
            elif start_index != -1 and pixel != block_color and pixel != background_color:
                 break # Stop if a different color block starts
            # If we hit background after finding a block, the block ended
            elif start_index != -1 and pixel == background_color:
                break 
        elif start_index != -1: # Found background after the block started
             break
             
    # Handle case where block goes to the very end
    # The loop above correctly sets end_index in this case

    return start_index, end_index, block_color

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Shifts the single contiguous block of non-background color in a 1xN grid 
    one position to the right.

    Args:
        input_grid: A list containing a single list representing the input row.

    Returns:
        A list containing a single list representing the transformed row.
    """
    # Ensure input is a list of lists and extract the single row
    if not isinstance(input_grid, list) or not input_grid or not isinstance(input_grid[0], list):
        # Handle invalid input format if necessary, though ARC guarantees grid format
        return [] 
        
    input_row = input_grid[0]
    height = len(input_grid) # should be 1
    width = len(input_row)
    background_color = 0 # Assuming white is always background based on examples

    # Initialize the output grid/row with the background color
    # Since it's 1D, we work with the row directly first
    output_row = [background_color] * width

    # Find the non-background block in the input row
    start_index, end_index, block_color = find_contiguous_block(input_row, background_color)

    # If a block is found, shift it one position to the right in the output row
    if start_index != -1:
        # Calculate new start and end indices for the shifted block
        new_start_index = start_index + 1
        new_end_index = end_index + 1

        # Copy the block to the new position, ensuring bounds are respected
        # The original block length is (end_index - start_index + 1)
        block_length = end_index - start_index + 1
        for i in range(block_length):
            # Check if the new position is within the grid bounds
            if new_start_index + i < width:
                # The color to copy is simply block_color
                output_row[new_start_index + i] = block_color
                
    # Wrap the output row back into a list of lists format
    output_grid = [output_row]
    
    return output_grid
