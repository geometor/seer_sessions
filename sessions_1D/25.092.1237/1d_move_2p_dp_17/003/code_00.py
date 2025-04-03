"""
Transforms the input grid according to the rule: 
1. Identify the single azure (8) pixel and keep it in the same position in the output.
2. Identify the first contiguous block of pixels that are not white (0) and not azure (8).
3. Shift this block 2 positions to the right in the output grid.
4. The azure pixel's position takes precedence; the shifted block does not overwrite it.
5. Fill the rest of the output grid with white (0).
"""

import numpy as np

def find_contiguous_block_np(grid_row, excluded_colors):
    """
    Finds the first contiguous block of pixels in a NumPy array 
    not matching the excluded colors.
    Returns the start index, length, and color of the block, or None if not found.
    
    Args:
        grid_row (np.ndarray): The 1D input array (row).
        excluded_colors (set): A set of colors to exclude from the block.

    Returns:
        tuple: (start_index, length, color) or None if no block found.
    """
    start_index = -1
    block_color = -1
    in_block = False
    grid_width = len(grid_row)

    for i, pixel in enumerate(grid_row):
        is_block_pixel = pixel not in excluded_colors
        
        if is_block_pixel and not in_block:
            # Start of a new block
            start_index = i
            block_color = pixel
            in_block = True
        elif not is_block_pixel and in_block:
            # End of the block (found an excluded color after being in a block)
            length = i - start_index
            return start_index, length, block_color
            # Note: We only find the *first* block, so we return immediately.

    # Check if the block extends to the end of the row
    if in_block:
        length = grid_width - start_index
        return start_index, length, block_color
        
    return None # No block found

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Ensure input is a NumPy array
    input_np = np.array(input_grid, dtype=int)
    
    # Assuming the grid is always 1xN
    if input_np.ndim == 1:
        input_row = input_np
    elif input_np.shape[0] == 1:
         input_row = input_np[0]
    else:
        # Handle potential malformed input if necessary, though ARC format is usually consistent
        raise ValueError("Input grid is not a 1xN grid")

    grid_width = len(input_row)

    # 1. Initialize the output grid with white (0) pixels.
    output_row = np.zeros(grid_width, dtype=int)

    # 2. Locate the position of the single azure (8) pixel.
    azure_indices = np.where(input_row == 8)[0]
    azure_pos = -1
    if len(azure_indices) > 0:
        azure_pos = azure_indices[0] # Take the first one if multiple exist (unlikely based on task)

    # 3. Place an azure (8) pixel at the same position in the output grid.
    if azure_pos != -1:
        output_row[azure_pos] = 8

    # 4. Identify the contiguous block (not white 0, not azure 8).
    block_info = find_contiguous_block_np(input_row, excluded_colors={0, 8})

    if block_info:
        start_index, length, color = block_info

        # 5. Calculate the new starting position for this block (shift right by 2).
        new_start_index = start_index + 2

        # 6. Place this contiguous block into the output grid at the new position.
        # Ensure we don't write past the grid boundary or over the azure pixel's fixed position.
        for i in range(length):
            target_index = new_start_index + i
            
            # Check grid bounds AND if the target position is not the azure pixel's fixed position
            if 0 <= target_index < grid_width and target_index != azure_pos:
                 output_row[target_index] = color

    # Return the output grid in the required list-of-lists format
    # Convert NumPy array row back to a list, then wrap in another list.
    return [output_row.tolist()]