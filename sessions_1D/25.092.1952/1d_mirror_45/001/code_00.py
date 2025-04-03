import numpy as np
import copy

"""
Transformation Rule Natural Language Description:

The transformation operates on a 1-dimensional grid (represented as a list or 1xN array). 
1. Identify the unique maroon pixel (value 9), which acts as a fixed pivot.
2. Locate a contiguous block of non-white (0), non-maroon (9) pixels situated to the left of the pivot. This block is always separated from the pivot by exactly one white pixel.
3. Move this identified block to the right side of the pivot.
4. The block's original position is filled with white pixels.
5. On the right side, the block is placed such that it is separated from the pivot by exactly one white pixel, mirroring the separation pattern from the input. Specifically, if the block ended at index `pivot_index - 2` in the input, it starts at index `pivot_index + 2` in the output.
6. The pivot pixel and all other white pixels remain in their original positions, except for those overwritten during the block's removal and placement.
"""

def find_pivot(grid_1d):
    """Finds the index of the pivot pixel (value 9)."""
    for i, pixel in enumerate(grid_1d):
        if pixel == 9:
            return i
    return -1 # Should not happen based on examples

def find_block_left(grid_1d, pivot_index):
    """
    Finds the contiguous block of non-white, non-maroon pixels
    to the left of the pivot, separated by one white pixel.
    Returns (start_index, end_index, block_pixels) or None if not found.
    """
    if pivot_index < 2 or grid_1d[pivot_index - 1] != 0:
        return None # Separator condition not met

    block_pixels = []
    block_start = -1
    block_end = -1
    block_color = -1

    # Search backwards from pivot_index - 2
    for i in range(pivot_index - 2, -1, -1):
        pixel_value = grid_1d[i]
        if pixel_value != 0 and pixel_value != 9:
            if block_color == -1: # First non-zero/non-nine pixel found
                block_color = pixel_value
                block_end = i
                block_start = i
                block_pixels.insert(0, pixel_value)
            elif pixel_value == block_color: # Continue the block
                block_start = i
                block_pixels.insert(0, pixel_value)
            else: # Different color or invalid pixel encountered, block ends here
                break
        elif block_color != -1: # Zero or nine encountered after block started
            break # Block ends here
        else: # Still searching (found 0 or 9 before block start)
            break # No block immediately before separator

    if block_start != -1:
        return block_start, block_end, block_pixels
    else:
        return None

def transform(input_grid):
    """
    Applies the transformation rule: moves a colored block from the left 
    of a pivot (9) to its right, maintaining a one-pixel white separation.

    Args:
      input_grid: A list of lists representing the input grid (expected 1xN).

    Returns:
      A list of lists representing the transformed grid.
    """
    
    # Ensure input is in a usable 1D format (list or numpy array)
    # ARC standard is list of lists, even for 1 row.
    if not isinstance(input_grid, list) or not input_grid or not isinstance(input_grid[0], list):
         # Handle unexpected format if necessary, or assume valid input
         # For simplicity, we'll assume it's a list containing one list (the row)
         pass 
         
    grid_1d = np.array(input_grid[0], dtype=int)
    output_grid_1d = grid_1d.copy()
    grid_width = len(grid_1d)

    # 1. Find the pivot index
    pivot_index = find_pivot(grid_1d)
    if pivot_index == -1:
        # If no pivot, return the original grid (or handle error)
        return input_grid 

    # 2. Find the block to the left of the pivot
    block_info = find_block_left(grid_1d, pivot_index)

    if block_info:
        block_start, block_end, block_pixels = block_info
        
        # 3. Erase the original block in the output grid
        output_grid_1d[block_start : block_end + 1] = 0

        # 4. Calculate the target position for the block on the right
        target_start = pivot_index + 2
        target_end = target_start + len(block_pixels)

        # 5. Place the block in the target position 
        # Check bounds just in case, though examples fit
        if target_end <= grid_width:
             # Ensure the target area is currently empty (white/0)
             # Although not explicitly stated, examples imply this space is available.
             # We will overwrite regardless, as per the observed transformation.
            output_grid_1d[target_start : target_end] = block_pixels
        else:
            # Handle out-of-bounds case if necessary
            # Based on examples, this shouldn't occur. Return partially modified grid or original?
            # Let's return the grid modified up to this point.
            pass 

    # Convert the result back to the standard ARC format (list of lists)
    return [output_grid_1d.tolist()]
