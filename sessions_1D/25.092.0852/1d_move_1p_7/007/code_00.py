import copy
from typing import List, Tuple

"""
Identifies the single contiguous block of non-background (non-white, color 0) 
colored pixels in the input row (a 1xN grid). Creates an output grid of the 
same dimensions, initially filled with the background color. Shifts (translates) 
the identified block one position horizontally to the right within the output grid. 
Vacated space is filled with the background color (which happens automatically 
by initializing the output grid with the background color). The color and length 
of the block are preserved. Assumes input is always 1xN.
"""

def find_block(row: List[int], background_color: int = 0) -> Tuple[int, int, int]:
    """
    Finds the start index, end index, and color of the first contiguous 
    block of non-background color in a 1D list (row).

    Args:
        row: The input list (row of the grid).
        background_color: The integer value representing the background color.

    Returns:
        A tuple containing (start_index, end_index, block_color).
        Returns (-1, -1, -1) if no block is found or the row is empty.
    """
    if not row:
        return -1, -1, -1 # Handle empty row

    start_index = -1
    end_index = -1
    block_color = -1
    
    # Iterate through pixels to find the block boundaries
    for i, pixel in enumerate(row):
        # If we find a non-background pixel and haven't started a block yet
        if pixel != background_color and start_index == -1:
            start_index = i
            end_index = i # Initialize end_index as the start
            block_color = pixel
        # If we are inside a block and the pixel matches the block color
        elif start_index != -1 and pixel == block_color:
            end_index = i # Extend the block's end index
        # If we are inside a block but encounter background or a *different* non-bg color
        elif start_index != -1 and (pixel == background_color or pixel != block_color):
            # The block ended just before this pixel
            break 

    # If no non-background pixel was ever found
    if start_index == -1:
        return -1, -1, -1
        
    return start_index, end_index, block_color

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by shifting the single non-background block right.
    """
    # --- Input Validation and Setup ---
    # Check if input is a list containing exactly one list (row)
    # Although ARC guarantees grid format, this ensures it's 1xN.
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        # Return a copy of the input if format is not 1xN as expected
        return copy.deepcopy(input_grid) 
        
    input_row = input_grid[0]
    width = len(input_row)
    
    # Handle empty row case explicitly
    if width == 0:
        return [[]] # Return an empty 1x0 grid

    background_color = 0 # Define background color (white)

    # --- Initialize Output ---
    # Create the output row, initially filled entirely with the background color
    output_row = [background_color] * width

    # --- Find the Object (Block) ---
    # Locate the contiguous block of non-background color in the input row using the helper
    start_index, end_index, block_color = find_block(input_row, background_color)

    # --- Apply Transformation ---
    # If no block was found (input row is all background), the initialized output_row is correct
    if start_index != -1:
        # Iterate through the indices of the original block in the input row
        for i in range(start_index, end_index + 1):
            # Calculate the target index in the output row (shifted right by 1)
            target_index = i + 1 
            
            # Check if the target index is within the grid bounds
            if target_index < width:
                # Place the block's color at the new, shifted position in the output row
                # Note: block_color holds the color identified by find_block
                output_row[target_index] = block_color
            # If target_index >= width, the block is partially or fully shifted off the grid,
            # so we don't place those parts. The output cell remains background color.

    # --- Format and Return Output ---
    # Wrap the processed output row back into the grid format (list of lists)
    output_grid = [output_row]
    
    return output_grid