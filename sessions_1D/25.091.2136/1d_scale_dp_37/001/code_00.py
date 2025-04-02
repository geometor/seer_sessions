import numpy as np
import copy

"""
Fill white space (0) between a contiguous block of a non-white (0), non-red (2) color (C) and the next red (2) marker using the color C.

1.  Find the end position of the first contiguous block of a color C (not 0 or 2).
2.  Find the position of the first red (2) marker after this block.
3.  If the pixels between the block's end and the red marker are all white (0), fill these pixels with color C.
"""

def find_first_block_end(grid):
    """Finds the end index and color of the first non-white, non-red block."""
    block_color = -1
    block_end_index = -1
    in_block = False

    for i, pixel in enumerate(grid):
        if not in_block:
            # Start of a potential block
            if pixel != 0 and pixel != 2:
                in_block = True
                block_color = pixel
                block_end_index = i
            # If we hit red before finding a block, stop searching for this pattern
            elif pixel == 2:
                 return -1, -1 # Indicate no valid block found before red
        else:
            # Continue block or end block
            if pixel == block_color:
                block_end_index = i
            else:
                # Block ended just before this pixel
                return block_color, block_end_index
    
    # If the block extends to the end of the grid
    if in_block:
        return block_color, block_end_index
    else:
        # No block found at all
         return -1, -1


def find_first_marker_after(grid, start_index, marker_color=2):
    """Finds the index of the first occurrence of marker_color after start_index."""
    for i in range(start_index + 1, len(grid)):
        if grid[i] == marker_color:
            return i
    return -1 # Marker not found

def check_gap_is_white(grid, start_index, end_index):
    """Checks if all pixels between start_index (exclusive) and end_index (exclusive) are white (0)."""
    # If no gap exists (indices are adjacent or invalid range)
    if start_index + 1 >= end_index:
        return True # No gap to check, condition met vacuously

    for i in range(start_index + 1, end_index):
        if grid[i] != 0:
            return False
    return True

def transform(input_grid):
    """
    Transforms the input grid by filling the white gap between the first
    non-white/non-red block and the subsequent red marker with the block's color.
    Assumes input_grid is a 1D list or numpy array.
    """
    # Ensure input is a list for easier manipulation if it's numpy
    if isinstance(input_grid, np.ndarray):
        # Handle potential multi-dimensional arrays, assuming the relevant data is in the first row
        if input_grid.ndim > 1:
             grid = input_grid[0].tolist() # Take the first row if multi-dimensional
        else:
             grid = input_grid.tolist()
    else:
        # Create a copy to avoid modifying the original input list
        grid = list(input_grid) # Use list() for shallow copy

    output_grid = list(grid) # Create a modifiable copy

    # 1. Find the end of the first relevant color block
    block_color, block_end_index = find_first_block_end(grid)

    # If no valid block was found, return the original grid copy
    if block_color == -1 or block_end_index == -1:
        return output_grid

    # 2. Find the first red marker (2) after the block
    red_marker_index = find_first_marker_after(grid, block_end_index, marker_color=2)

    # If no red marker was found after the block, return the original grid copy
    if red_marker_index == -1:
        return output_grid

    # 3. Check if the gap between the block and the marker is entirely white (0)
    is_gap_white = check_gap_is_white(grid, block_end_index, red_marker_index)

    # 4. If the gap is white, fill it with the block's color
    if is_gap_white:
        # Iterate from the pixel *after* the block up to (but not including) the red marker
        for i in range(block_end_index + 1, red_marker_index):
             # Only modify if the original pixel was white (although check_gap_is_white should ensure this)
             if grid[i] == 0:
                 output_grid[i] = block_color

    # 5. Return the modified grid
    return output_grid