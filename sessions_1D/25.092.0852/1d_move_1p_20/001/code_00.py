import numpy as np
from typing import List, Tuple, Optional

"""
Transformation Rule:
1. Identify the single contiguous block of non-white pixels in the input row.
2. Determine the start and end indices of this block.
3. If the block starts at index 0 (no preceding white pixel), return the input unchanged.
4. Otherwise, shift the entire block one position to the right.
5. Move the white pixel that was immediately preceding the block (at start_index - 1) into the original starting position of the block (at start_index).
"""

def find_non_white_block(row: List[int]) -> Optional[Tuple[int, int]]:
    """
    Finds the start and end index of the first contiguous block of non-white pixels.

    Args:
        row: A list of integers representing a row of the grid.

    Returns:
        A tuple (start_index, end_index) if a block is found, otherwise None.
    """
    start_index = -1
    end_index = -1
    for i, pixel in enumerate(row):
        if pixel != 0:
            if start_index == -1:
                start_index = i
            end_index = i
        elif start_index != -1:
            # Block ended
            break
    if start_index != -1:
        return start_index, end_index
    return None

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Shifts a contiguous block of non-white pixels one step right,
    moving the preceding white pixel into the block's original start position.

    Args:
        input_grid: A 2D list representing the input grid (expected to be 1xN).

    Returns:
        A 2D list representing the transformed grid.
    """
    # Ensure input is a single row grid
    if not input_grid or len(input_grid) != 1:
        # Handle empty or multi-row grids if necessary, returning input for now
        return input_grid
        
    input_row = input_grid[0]
    n = len(input_row)
    
    # Initialize output_row as a copy of the input row
    output_row = list(input_row) 

    # Find the contiguous block of non-white pixels
    block_indices = find_non_white_block(input_row)

    if block_indices:
        start_index, end_index = block_indices
        
        # Check if there is a preceding white pixel and space to shift
        if start_index > 0 and end_index + 1 < n:
            # Store the block pixels
            block_pixels = input_row[start_index : end_index + 1]
            
            # Shift the block one position to the right in the output row
            # This overwrites the original block start and the pixel after the block end
            for i in range(len(block_pixels)):
                 output_row[start_index + 1 + i] = block_pixels[i]
                 
            # Place the preceding white pixel (which is always 0) 
            # at the original start position of the block
            output_row[start_index] = 0 
            
    # Wrap the output row back into the grid format
    output_grid = [output_row]
    return output_grid
