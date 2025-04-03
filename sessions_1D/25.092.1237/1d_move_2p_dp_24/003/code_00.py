import numpy as np
from typing import List, Tuple, Optional

"""
Transformation Rule:
1. Locate the unique target pixel (green=3) in the 1D input NumPy array.
2. Identify the block of two background pixels (white=0) immediately to the left of the target pixel. This is the 'fixed gap'.
3. Identify the contiguous block of a single non-white, non-green color located immediately to the left of the fixed gap. This is the 'movable block'.
4. Determine the start and end indices of the movable block.
5. Construct the output array by rearranging segments:
   a. Pixels originally before the movable block.
   b. The two white background pixels (representing the gap shifted left).
   c. The movable block pixels.
   d. The target pixel.
   e. Pixels originally after the target pixel.
Essentially, the movable block shifts right by two positions, closing the gap next to the target pixel, and the gap (two white pixels) fills the space where the block started its shift.
"""

def find_target_pixel_np(grid: np.ndarray, target_color: int) -> Optional[int]:
    """
    Finds the index of the first occurrence of the target color in a 1D NumPy array.
    Returns the index or None if not found.
    """
    indices = np.where(grid == target_color)[0]
    if len(indices) > 0:
        return indices[0]  # Return the first index found
    return None

def find_movable_block_np(grid: np.ndarray, target_index: int, background_color: int) -> Optional[Tuple[int, int]]:
    """
    Finds the start and end indices of the movable block based on its expected position
    relative to the target pixel and the fixed gap of size 2.
    Returns (start_index, end_index) or None if the structure is not found.
    """
    # Expected end of the block is 3 positions left of the target
    expected_block_end_index = target_index - 3
    
    # Basic boundary checks
    if expected_block_end_index < 0:
        print(f"Error: Expected block end index {expected_block_end_index} is out of bounds.")
        return None
        
    # Check if the gap pixels are indeed background color
    if target_index < 2 or grid[target_index - 1] != background_color or grid[target_index - 2] != background_color:
        print(f"Error: Expected gap pixels at {target_index - 1}, {target_index - 2} are not background color.")
        return None
        
    # Get the color of the block
    block_color = grid[expected_block_end_index]
    
    # Check if block color is valid (not background, not target)
    # Note: target_color check isn't strictly needed based on problem description, but good practice.
    if block_color == background_color: # or block_color == target_color:
        print(f"Error: Pixel at expected block end {expected_block_end_index} is background color.")
        return None

    # Scan left from the block end to find the start of the block
    block_start_index = expected_block_end_index
    current_index = expected_block_end_index - 1
    while current_index >= 0 and grid[current_index] == block_color:
        block_start_index = current_index
        current_index -= 1
        
    return block_start_index, expected_block_end_index


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input 1D NumPy array.
    Finds a target pixel (3), identifies a block to its left separated by a gap of 2,
    and shifts the block right by 2 positions to close the gap.
    """
    
    # Configuration
    target_color = 3
    background_color = 0
    gap_size = 2

    # 1. Find the target pixel index
    target_index = find_target_pixel_np(input_grid, target_color)
    
    if target_index is None:
        print(f"Error: Target color {target_color} not found.")
        return input_grid.copy() # Return a copy of the input if target not found

    # 2. Find the movable block's start and end indices
    block_indices = find_movable_block_np(input_grid, target_index, background_color)

    if block_indices is None:
         print(f"Error: Could not find the expected movable block structure.")
         # Handle case where block/gap structure isn't as expected
         return input_grid.copy() # Return a copy of the input

    block_start_index, block_end_index = block_indices

    # 3. Extract the different segments of the input grid using NumPy slicing
    pixels_before_block = input_grid[:block_start_index]
    movable_block_pixels = input_grid[block_start_index : block_end_index + 1]
    # The gap pixels are implicitly input_grid[block_end_index + 1 : target_index]
    target_pixel = input_grid[target_index:target_index+1] # Use slice to keep it as an array
    pixels_after_target = input_grid[target_index + 1:]

    # 4. Define the new gap segment (to be placed where the block started shifting)
    new_gap_segment = np.full(gap_size, background_color, dtype=input_grid.dtype)

    # 5. Construct the output grid by concatenating segments in the new order
    # Order: (Pixels before block) + (New gap) + (Movable block) + (Target pixel) + (Pixels after target)
    output_grid = np.concatenate((
        pixels_before_block,
        new_gap_segment,
        movable_block_pixels,
        target_pixel,
        pixels_after_target
    ))

    return output_grid