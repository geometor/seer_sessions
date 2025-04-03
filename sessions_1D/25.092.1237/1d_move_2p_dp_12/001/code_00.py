"""
Transforms a 1D grid by shifting a contiguous colored block (not white or red) 
and a single red pixel two positions to the right, filling the vacated space 
with white (0). The relative positions of the block and the red pixel, 
including the two white pixels separating them, are maintained.
"""

import numpy as np

def find_block(grid_row):
    """Finds the start index, end index, and color of the non-white, non-red block."""
    block_start = -1
    block_end = -1
    block_color = -1
    for i, pixel in enumerate(grid_row):
        if pixel != 0 and pixel != 2:  # Found the start of the block
            block_start = i
            block_color = pixel
            # Find the end of the block
            for j in range(i, len(grid_row)):
                if grid_row[j] == block_color:
                    block_end = j
                else:
                    break # Block ended
            break # Found the block, no need to continue outer loop
    return block_start, block_end, block_color

def find_pixel(grid_row, color):
    """Finds the index of the first pixel with the specified color."""
    for i, pixel in enumerate(grid_row):
        if pixel == color:
            return i
    return -1 # Not found

def transform(input_grid):
    """
    Applies the transformation rule: shifts a colored block and a red pixel 
    two positions to the right.

    Args:
        input_grid (list of lists or numpy array): The input grid (1 row).

    Returns:
        numpy array: The transformed grid.
    """
    # Ensure input is a numpy array for easier slicing
    input_array = np.array(input_grid, dtype=int)
    
    # Since it's 1D, we work with the first row
    input_row = input_array[0]
    grid_length = len(input_row)

    # Initialize output_grid with background color (white, 0)
    output_grid = np.zeros_like(input_array)
    output_row = output_grid[0]

    # 1. Identify the contiguous block of non-white, non-red colored pixels
    block_start, block_end, block_color = find_block(input_row)
    
    # 2. Identify the position of the single red (2) pixel
    red_pixel_index = find_pixel(input_row, 2)

    # Check if both objects were found (as expected from examples)
    if block_start != -1 and red_pixel_index != -1:
        # 3. Calculate new positions (shift right by 2)
        new_block_start = block_start + 2
        new_block_end = block_end + 2
        new_red_pixel_index = red_pixel_index + 2

        # Ensure new positions are within bounds (although examples suggest they always are)
        if new_block_end < grid_length and new_red_pixel_index < grid_length:
            # 4. Copy the block to the output grid at the new position
            block_length = block_end - block_start + 1
            output_row[new_block_start : new_block_start + block_length] = input_row[block_start : block_end + 1]
            
            # 5. Place the red pixel in the output grid at the new position
            output_row[new_red_pixel_index] = 2
        else:
            # Handle potential out-of-bounds shift if necessary, 
            # though not seen in examples. For now, just proceed.
            # If strict boundary checking is needed, add logic here.
             # 4. Copy the block to the output grid at the new position (handling potential clipping)
            block_length = block_end - block_start + 1
            copy_len = min(block_length, grid_length - new_block_start)
            if copy_len > 0:
                 output_row[new_block_start : new_block_start + copy_len] = input_row[block_start : block_start + copy_len]
            
            # 5. Place the red pixel in the output grid at the new position (handling potential clipping)
            if new_red_pixel_index < grid_length:
                output_row[new_red_pixel_index] = 2


    # 6. Return the modified output grid
    return output_grid.tolist() # Return as list of lists per ARC standard