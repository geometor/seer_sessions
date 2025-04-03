import numpy as np
from typing import List

"""
Transformation Rule:
1. Locate the unique target pixel (green=3).
2. Identify the contiguous block of non-background (non-white=0) pixels immediately to the left of the target pixel. This is the 'movable block'.
3. Identify the contiguous block of background (white=0) pixels, if any, situated between the movable block and the target pixel. This is the 'gap'.
4. Determine the size of the gap (number of white pixels).
5. Shift the 'movable block' to the right by a distance equal to the size of the gap, effectively closing the gap and making the movable block adjacent to the target pixel.
6. The relative order and content of all other pixels (background pixels before the movable block, the target pixel itself, and pixels after the target pixel) remain unchanged.
"""

def find_target_pixel(grid: List[int], target_color: int) -> int:
    """Finds the index of the first occurrence of the target color."""
    try:
        return grid.index(target_color)
    except ValueError:
        raise ValueError(f"Target color {target_color} not found in grid.")

def find_movable_block_and_gap(grid: List[int], target_index: int) -> tuple[int, int, int]:
    """
    Finds the start and end indices of the movable block and the size of the gap.
    Scans leftwards from the target pixel.
    Returns (block_start_index, block_end_index, gap_size).
    """
    block_end_index = -1
    gap_size = 0
    
    # Scan left from the target to find the end of the block and the gap
    current_index = target_index - 1
    while current_index >= 0 and grid[current_index] == 0:
        gap_size += 1
        current_index -= 1
        
    # If we found non-background pixels, the last non-background index is the block end
    if current_index >= 0 and grid[current_index] != 0:
        block_end_index = current_index
        block_color = grid[block_end_index]
    else:
        # No movable block found immediately preceded by only background
        # Or the block is at the very beginning after background
        if current_index >= 0 : # found non-zero block_color before potential gap
             block_end_index = current_index
        else: # reached beginning of array while only seeing 0s
            # This case might indicate no movable block or an error in assumptions
            # Based on examples, there's always a block. Let's assume block_end_index must be >= 0.
            # If block_end_index remains -1, it implies no block was found left of the target separated only by optional whitespace.
            # This shouldn't happen based on provided examples.
             raise ValueError("Could not find end of movable block.")


    # Scan left from the block end to find the start of the block
    block_start_index = block_end_index
    block_color = grid[block_end_index]
    current_index = block_end_index - 1
    while current_index >= 0 and grid[current_index] == block_color:
        block_start_index = current_index
        current_index -= 1
        
    return block_start_index, block_end_index, gap_size

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input grid (1D list).
    Finds a target pixel (3), identifies a block to its left, measures the gap
    between them, and shifts the block right to close the gap.
    """
    
    # Configuration
    target_color = 3
    background_color = 0

    # 1. Find the target pixel
    try:
        target_index = find_target_pixel(input_grid, target_color)
    except ValueError as e:
        print(f"Error: {e}")
        # Decide how to handle missing target: return input? raise error?
        return input_grid # Or raise e

    # 2. Find the movable block and the gap size
    try:
        block_start_index, block_end_index, gap_size = find_movable_block_and_gap(input_grid, target_index)
    except ValueError as e:
         print(f"Error: {e}")
         # Handle case where block/gap structure isn't as expected
         return input_grid # Or raise e

    # If gap_size is 0, the block is already adjacent, no transformation needed
    if gap_size == 0:
        return input_grid[:] # Return a copy

    # 3. Extract the different segments of the input grid
    pixels_before_block = input_grid[:block_start_index]
    movable_block_pixels = input_grid[block_start_index : block_end_index + 1]
    # Gap pixels are implicitly handled by the gap_size
    target_pixel = [input_grid[target_index]] # Should be [target_color]
    pixels_after_target = input_grid[target_index + 1:]

    # 4. Construct the output grid
    # New arrangement: pixels before block + new gap (at original block location) + block + target + pixels after target
    
    # Create the filler for the space originally occupied by the block start
    newly_empty_space = [background_color] * gap_size 
    
    output_grid = pixels_before_block + newly_empty_space + movable_block_pixels + target_pixel + pixels_after_target

    return output_grid
