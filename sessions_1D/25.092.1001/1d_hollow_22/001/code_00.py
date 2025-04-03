import numpy as np
from typing import List

"""
Transformation Rule:
1. Identify the contiguous horizontal block of non-white pixels in the input 1D array.
2. Determine the starting index, ending index, and color of this block.
3. Create an output array of the same size, initialized to all white (0).
4. Place the identified block's color at the starting index in the output array.
5. Place the identified block's color at the ending index in the output array.
6. All other pixels in the output array remain white (0).
"""

def find_non_white_block_indices(grid_1d: List[int]) -> tuple[int | None, int | None, int | None]:
    """
    Finds the start index, end index, and color of the first contiguous 
    non-white block in a 1D list. Assumes only one such block exists.
    
    Args:
        grid_1d: A list of integers representing pixels.
        
    Returns:
        A tuple (start_index, end_index, color). Returns (None, None, None) 
        if no non-white block is found.
    """
    start_index = None
    end_index = None
    block_color = None
    
    # Find the first non-white pixel
    for i, pixel in enumerate(grid_1d):
        if pixel != 0:
            start_index = i
            block_color = pixel
            break
            
    # If no non-white pixel found, return None
    if start_index is None:
        return None, None, None
        
    # Find the last non-white pixel (must be the same color for a contiguous block)
    # Iterate backwards to find the last occurrence efficiently,
    # or simply update end_index whenever we see the block_color.
    for i in range(start_index, len(grid_1d)):
         # Update end_index if we are still in the block
         if grid_1d[i] == block_color:
             end_index = i
         # If we encounter a different non-zero color or a zero after starting,
         # the block has ended. (Assumes single contiguous block)
         elif grid_1d[i] != block_color:
              break # Stop searching once the block ends

    # Re-confirm end_index by searching backwards if the forward search felt ambiguous
    # Let's stick to the simpler forward update logic based on the examples.
    # Find the last index matching the block_color starting from the end
    for i in range(len(grid_1d) - 1, start_index - 1, -1):
        if grid_1d[i] == block_color:
            end_index = i
            break
            
    return start_index, end_index, block_color

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input 1D grid.
    Keeps only the first and last pixels of the non-white block, 
    turning the intermediate pixels white.

    Args:
        input_grid: A list of integers representing the input row/column.

    Returns:
        A list of integers representing the transformed row/column.
    """
    
    # Initialize output grid with the same size as input, filled with white (0)
    output_grid = [0] * len(input_grid)
    
    # Find the boundaries and color of the non-white block
    start_index, end_index, block_color = find_non_white_block_indices(input_grid)
    
    # If a block was found, place its endpoints in the output grid
    if start_index is not None and end_index is not None and block_color is not None:
        # Place the color at the start index
        output_grid[start_index] = block_color
        
        # Place the color at the end index (handles blocks of length 1 correctly)
        output_grid[end_index] = block_color
        
    # Pixels outside the original block's start/end indices, 
    # and pixels between start and end (exclusive) remain white (0) 
    # as initialized.
        
    return output_grid
