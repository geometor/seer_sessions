import numpy as np
from typing import List, Tuple

"""
Identifies the single contiguous block of non-white pixels in the input row.
Shifts this block one position to the right.
Creates a new output row of the same dimensions, filled with the background color (white/0).
Places the shifted block into the new output row.
"""

def find_non_white_block(row: List[int]) -> Tuple[int, int, int, int]:
    """
    Finds the start index, end index, length, and color of the first 
    contiguous block of non-white pixels in a row.

    Args:
        row: A list of integers representing the pixels in the row.

    Returns:
        A tuple containing:
        - start_index: The starting index of the block.
        - end_index: The ending index of the block.
        - length: The length of the block.
        - color: The color of the block pixels.
        Returns (-1, -1, 0, -1) if no non-white block is found.
    """
    start_index = -1
    end_index = -1
    color = -1
    length = 0
    
    for i, pixel in enumerate(row):
        if pixel != 0: # Found a non-white pixel
            if start_index == -1: # Start of a new block
                start_index = i
                color = pixel
            # Check if the pixel color matches the current block color
            if color == pixel:
                 end_index = i # Update end_index as long as we are in the block
            else: # Found a different color, stop searching (assuming only one block)
                 break
        elif start_index != -1: # Found a white pixel after the block started
            break # End of the block

    if start_index != -1:
        length = end_index - start_index + 1
        
    return start_index, end_index, length, color

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by shifting the single non-white horizontal block 
    one position to the right.

    Args:
        input_grid: A list containing a single list of integers (representing a 1xN grid).

    Returns:
        A new list containing a single list of integers (the transformed 1xN grid).
    """
    # Input is expected to be a 1xN grid, extract the single row
    if not input_grid or not isinstance(input_grid, list) or len(input_grid) != 1:
         # Handle invalid input format if necessary, though ARC ensures valid formats
         # For now, assume valid 1xN input based on examples
         return [] 
         
    input_row = input_grid[0]
    height = 1
    width = len(input_row)
    background_color = 0

    # Find the non-white block in the input row
    start_index, end_index, length, color = find_non_white_block(input_row)

    # Initialize the output grid (row) with the background color
    output_row = [background_color] * width

    # If a block was found, place it in the output row, shifted one position right
    if start_index != -1:
        new_start_index = start_index + 1
        # Ensure the new position is within bounds (though examples suggest it always is)
        if new_start_index + length <= width:
            for i in range(length):
                output_row[new_start_index + i] = color

    # Return the output row wrapped in a list to match the grid format
    return [output_row]
