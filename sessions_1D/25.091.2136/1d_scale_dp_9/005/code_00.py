"""
Transformation Rule:
Identifies the first contiguous block of non-white color and the first magenta (6) marker pixel in a single row input grid.
If both are found and the marker pixel's index is at least two positions greater than the block's end index, it fills the white (0) pixels located strictly between the end of the color block and the magenta marker pixel with the color of the block.
Otherwise, the input grid is returned unchanged.
"""

import numpy as np
from typing import List, Tuple, Optional

def find_first_color_block_end(row: np.ndarray) -> Optional[Tuple[int, int]]:
    """
    Finds the color and the index of the last pixel of the first contiguous 
    block of non-white (non-zero) color encountered when scanning from left to right.

    Args:
        row: A 1D numpy array representing the row of pixels.

    Returns:
        A tuple containing:
        - The color of the block (int).
        - The index of the last pixel of the block (int).
        Returns None if no non-white block is found.
    """
    block_color = -1
    block_end_index = -1
    in_block = False
    for i, pixel in enumerate(row):
        # If we encounter a non-white pixel and we are not currently in a block,
        # this marks the start of the *first* block.
        if pixel != 0 and not in_block: 
            block_color = pixel
            in_block = True
            block_end_index = i 
        # If we are in a block and the current pixel matches the block's color,
        # update the end index.
        elif in_block and pixel == block_color: 
            block_end_index = i 
        # If we are in a block and the current pixel does *not* match the block's color
        # (it could be white or another color), the block has ended. Return its info.
        elif in_block and pixel != block_color: 
            return int(block_color), int(block_end_index) 
    
    # If the loop finishes and we were tracking a block (meaning it extended to the end of the row),
    # return the last known information.
    if in_block:
        return int(block_color), int(block_end_index)
        
    # If no non-white pixel was ever encountered, return None.
    return None 

def find_marker(row: np.ndarray, marker_color: int = 6) -> Optional[int]:
    """
    Finds the index of the first occurrence of the marker pixel color.

    Args:
        row: A 1D numpy array representing the row of pixels.
        marker_color: The integer value of the color to find (default is 6 for magenta).

    Returns:
        The index of the first occurrence of the marker pixel, or None if not found.
    """
    # Find all indices where the pixel matches the marker color
    indices = np.where(row == marker_color)[0]
    # If any such indices were found, return the first one
    if len(indices) > 0:
        return int(indices[0]) 
    # Otherwise, the marker was not found
    return None 

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid: A list containing a single list of integers (representing a 1xN grid).

    Returns:
        A list containing a single list of integers representing the transformed grid.
    """
    # Ensure input is a single row grid, otherwise return it unchanged
    if not input_grid or len(input_grid) != 1:
        return input_grid 

    # Convert the input row to a numpy array for efficient processing
    input_row = np.array(input_grid[0], dtype=int)
    
    # Initialize the output row as a copy of the input row
    output_row = input_row.copy()

    # Step 2: Find the first non-white color block
    block_info = find_first_color_block_end(input_row)
    
    # If no block is found, return the original grid copy
    if block_info is None:
        return [output_row.tolist()]
        
    fill_color, block_end_index = block_info

    # Step 3: Find the magenta marker pixel
    marker_index = find_marker(input_row, 6)
    
    # If no marker is found, return the original grid copy
    if marker_index is None:
        return [output_row.tolist()]

    # Step 4: Check if the marker is positioned correctly for filling
    # The marker must be at least two indices away from the block's end
    # (i.e., there must be at least one pixel strictly between them)
    if marker_index > block_end_index + 1:
        
        # Step 5 & 6: Iterate through the indices in the "fill zone"
        # The zone starts one index after the block ends and ends one index before the marker.
        fill_start_index = block_end_index + 1
        fill_end_index = marker_index # The range function excludes the end index

        for i in range(fill_start_index, fill_end_index):
            # Check if the pixel in the *original* input row at this index is white (0)
            if input_row[i] == 0:
                 # If it's white, change the corresponding pixel in the *output* row to the fill color
                 output_row[i] = fill_color

    # Step 7: Return the modified row, formatted back into the required list-of-lists structure
    return [output_row.tolist()]