import numpy as np
from typing import List, Tuple

"""
Identifies a single contiguous block of non-white pixels in a 1D input grid (single row).
Shifts this block one position to the right.
The output grid has the same dimensions as the input grid, filled with the background color (white, 0),
and the shifted block placed accordingly.
"""

def find_contiguous_block(row: List[int]) -> Tuple[int, int, List[int]]:
    """
    Finds the start index, end index (exclusive), and pixel values of the first 
    contiguous block of non-white pixels in a row.

    Args:
        row: A list of integers representing the pixels in the row.

    Returns:
        A tuple containing:
        - start_index: The starting index of the block. Returns -1 if no block found.
        - end_index: The ending index (exclusive) of the block. Returns -1 if no block found.
        - block_pixels: A list of the pixel values within the block. Returns empty list if no block found.
    """
    start_index = -1
    end_index = -1
    block_pixels = []
    
    for i, pixel in enumerate(row):
        if pixel != 0:  # Found the start of a block
            start_index = i
            break
            
    if start_index != -1:
        for j in range(start_index, len(row)):
            if row[j] != 0:
                block_pixels.append(row[j])
            else: # Found the end of the block
                end_index = j
                break
        # If the block extends to the end of the row
        if end_index == -1 and start_index != -1:
             end_index = len(row)
             
    # Correct end_index if block goes to the very end and loop didn't set it
    if start_index != -1 and end_index == -1:
        end_index = len(row)

    return start_index, end_index, block_pixels


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by shifting the single non-white block one position to the right.

    Args:
        input_grid: A list containing a single list of integers representing the input row.

    Returns:
        A list containing a single list of integers representing the transformed row.
    """
    # Assume input is always 1xN
    input_row = input_grid[0]
    height = len(input_grid) # Should be 1
    width = len(input_row)

    # Initialize output grid with background color (white, 0)
    # Note: Creating a list of lists even for 1D to match ARC format
    output_grid = [[0 for _ in range(width)] for _ in range(height)] 
    output_row = output_grid[0] # Work with the actual row

    # Find the contiguous block of non-white pixels
    start_index, end_index, block_pixels = find_contiguous_block(input_row)

    # If a block was found
    if start_index != -1:
        # Calculate the new starting position (shifted one to the right)
        new_start_index = start_index + 1
        new_end_index = new_start_index + len(block_pixels) # Calculate new end based on length

        # Place the block in the output row at the new position
        # Ensure the block doesn't go out of bounds on the right
        if new_end_index <= width:
             for i in range(len(block_pixels)):
                 output_row[new_start_index + i] = block_pixels[i]
        # else: block would partially or fully shift off the grid, leave output white in that area (as per examples)
        
    # Return the modified output grid
    return output_grid