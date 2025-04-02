import numpy as np
from typing import List, Tuple, Optional

"""
Transformation Rule:
1. Identify the contiguous block of a single non-white (0), non-gray (5) color. Record its color and the index of its last pixel.
2. Identify the index of the single gray (5) pixel.
3. Fill the gap between the end of the colored block and the gray pixel with the block's color. Specifically, change any white (0) pixels located at indices strictly greater than the block's end index and strictly less than the gray pixel's index to the block's color.
"""

def find_colored_block(grid: List[int]) -> Optional[Tuple[int, int, int]]:
    """
    Finds the first contiguous block of a single color other than white (0) or gray (5).

    Args:
        grid: The input sequence (list of integers).

    Returns:
        A tuple containing (color, start_index, end_index) of the block,
        or None if no such block is found.
    """
    start_index = -1
    block_color = -1
    for i, pixel in enumerate(grid):
        if pixel != 0 and pixel != 5:
            if start_index == -1:
                start_index = i
                block_color = pixel
            elif pixel != block_color: # End of block if color changes
                 return block_color, start_index, i - 1
        elif start_index != -1: # End of block if white or gray encountered
            return block_color, start_index, i - 1
            
    # If the block extends to the end of the grid
    if start_index != -1:
        return block_color, start_index, len(grid) - 1
        
    return None # No block found

def find_gray_pixel_index(grid: List[int]) -> Optional[int]:
    """
    Finds the index of the first gray (5) pixel.

    Args:
        grid: The input sequence (list of integers).

    Returns:
        The index of the gray pixel, or None if not found.
    """
    for i, pixel in enumerate(grid):
        if pixel == 5:
            return i
    return None

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input grid (sequence).

    Args:
        input_grid: A list of integers representing the input sequence.

    Returns:
        A list of integers representing the transformed output sequence.
    """
    # Initialize output_grid as a copy of the input
    output_grid = list(input_grid)

    # Find the main colored block
    block_info = find_colored_block(output_grid)
    if not block_info:
        # No colored block found, return original grid
        return output_grid
        
    block_color, _, end_index = block_info

    # Find the gray pixel
    gray_index = find_gray_pixel_index(output_grid)
    if gray_index is None:
         # No gray pixel found, return original grid
        return output_grid

    # Ensure the gray pixel is after the block end
    if gray_index <= end_index:
        # Invalid configuration according to observed pattern, return original
        return output_grid

    # Iterate through the pixels between the block end and the gray pixel
    # Indices are from end_index + 1 up to (but not including) gray_index
    for i in range(end_index + 1, gray_index):
        # If the pixel is white, change it to the block color
        # Based on examples, it seems *all* pixels in the gap change, not just white ones.
        # Let's modify to match the example outputs directly.
        # if output_grid[i] == 0: # Original interpretation based on NL
        output_grid[i] = block_color # Revised interpretation based on examples

    return output_grid