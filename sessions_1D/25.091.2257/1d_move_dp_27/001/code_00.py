"""
Move a contiguous block of non-white, non-maroon colored pixels horizontally
to the right until its rightmost pixel is immediately adjacent to the left of
the fixed maroon (9) anchor pixel. The original position of the block is
filled with white (0) pixels. The anchor pixel and any pixels to its right
remain unchanged.
"""

import numpy as np

def find_moving_block(grid):
    """
    Finds the first contiguous block of non-white, non-maroon pixels.

    Args:
        grid (np.array): The input grid (1D array).

    Returns:
        tuple: (start_index, end_index, color, length) or None if not found.
    """
    block_start = -1
    block_color = -1
    for i, pixel in enumerate(grid):
        if pixel != 0 and pixel != 9:
            if block_start == -1:
                block_start = i
                block_color = pixel
            elif pixel != block_color: # End of block if color changes
                 return (block_start, i - 1, block_color, i - block_start)
        elif block_start != -1: # End of block if 0 or 9 is encountered
            return (block_start, i - 1, block_color, i - block_start)
    # If the block extends to the end of the grid
    if block_start != -1:
        return (block_start, len(grid) - 1, block_color, len(grid) - block_start)
    return None # Block not found

def find_anchor_pixel(grid):
    """
    Finds the index of the maroon (9) anchor pixel.

    Args:
        grid (np.array): The input grid (1D array).

    Returns:
        int: The index of the anchor pixel, or -1 if not found.
    """
    for i, pixel in enumerate(grid):
        if pixel == 9:
            return i
    return -1

def transform(input_grid):
    """
    Transforms the input grid by moving a colored block next to a maroon anchor.

    Args:
        input_grid (np.array): A 1xN numpy array representing the input grid.

    Returns:
        np.array: The transformed 1xN numpy array.
    """
    # Ensure input is a 1D array for easier processing
    # Note: ARC grids are technically 2D, but these examples are 1xN
    if input_grid.shape[0] != 1:
         raise ValueError("Input grid must be 1xN for this transformation.")
    grid_1d = input_grid[0] # Work with the 1D array

    # Initialize output_grid as a copy of the input grid's 1D representation
    output_grid_1d = grid_1d.copy()

    # 1. Identify the "Moving Block"
    block_info = find_moving_block(grid_1d)
    if block_info is None:
        # No block found, return original grid (or handle as error)
        return input_grid # Return original 2D shape

    block_start, block_end, block_color, block_length = block_info

    # 2. Identify the "Anchor Pixel"
    anchor_index = find_anchor_pixel(grid_1d)
    if anchor_index == -1:
        # No anchor found, return original grid (or handle as error)
        return input_grid # Return original 2D shape

    # 3. Clear the original position of the Moving Block
    output_grid_1d[block_start : block_end + 1] = 0 # Fill with white

    # 4. Calculate the new position for the Moving Block
    new_block_end = anchor_index - 1
    new_block_start = new_block_end - block_length + 1

    # Ensure the new position is valid
    if new_block_start < 0:
         print(f"Warning: Calculated new block start index ({new_block_start}) is out of bounds. Clipping.")
         # This case shouldn't happen based on examples, but handle defensively
         new_block_start = 0 # Adjust start, potentially truncating block visually
         # Recalculate end based on potentially truncated length
         actual_length_to_place = new_block_end - new_block_start + 1
         if actual_length_to_place < block_length:
              print(f"Warning: Block truncated due to boundary collision.")
         # We'll still use block_color for the available space

    # 5. Place the Moving Block in its new position
    # Ensure we don't write past the calculated end index
    # This also handles potential truncation if new_block_start was clipped to 0
    output_grid_1d[new_block_start : new_block_end + 1] = block_color

    # Reshape back to 1xN before returning
    return output_grid_1d.reshape(1, -1)