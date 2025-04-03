import numpy as np
from typing import List, Tuple

"""
Identifies a single contiguous block of non-white pixels in a 1D input grid (single row) 
and shifts this block exactly two positions to the right in the output grid. 
The background remains white (0). Pixels shifted off the right edge are lost, 
and the space vacated by the block's original position becomes white.
"""

def find_non_background_block(row: List[int], background_color: int = 0) -> Tuple[int, int, int, int]:
    """
    Finds the start index, end index, color, and length of the first contiguous
    block of non-background pixels in a 1D list.

    Args:
        row: The input list representing the grid row.
        background_color: The integer value representing the background color.

    Returns:
        A tuple containing (start_col, end_col, color, length).
        Returns (-1, -1, -1, 0) if no non-background block is found.
    """
    start_col = -1
    end_col = -1
    color = -1
    length = 0
    
    for i, pixel in enumerate(row):
        if pixel != background_color:
            if start_col == -1:
                start_col = i
                color = pixel
            # Continue as long as the color matches the first found non-bg color
            if color == pixel:
                 end_col = i
            else: # Found a different non-bg color, stop (only one block expected)
                break
        elif start_col != -1: # Found background after starting a block
             break # End of the block

    if start_col != -1:
        length = end_col - start_col + 1
        return start_col, end_col, color, length
    else:
        return -1, -1, -1, 0


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Shifts the single non-white block in a 1D input grid two positions to the right.

    Args:
        input_grid: A list containing a single list of integers representing the 1D grid.

    Returns:
        A list containing a single list of integers representing the transformed 1D grid.
    """
    
    # Input is expected to be 1D, represented as [[...]]
    if not input_grid or len(input_grid) != 1:
        # Handle empty or incorrectly formatted input if necessary, 
        # though ARC examples usually conform.
        return input_grid 
        
    input_row = input_grid[0]
    height = 1
    width = len(input_row)
    background_color = 0 # white

    # Initialize output_grid as a copy first or fill with background
    # Create an empty output row filled with the background color
    output_row = [background_color] * width

    # Find the non-background block
    start_col, end_col, color, length = find_non_background_block(input_row, background_color)

    # If a block was found
    if start_col != -1:
        # Calculate the new starting position
        new_start_col = start_col + 2
        
        # Copy the block to the new position in the output row
        # Iterate through the length of the original block
        for i in range(length):
            current_output_col = new_start_col + i
            # Check if the new position is within the grid bounds
            if 0 <= current_output_col < width:
                output_row[current_output_col] = color

    # Format the output row back into the grid structure
    output_grid = [output_row]
    
    return output_grid