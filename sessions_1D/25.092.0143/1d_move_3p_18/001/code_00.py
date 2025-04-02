import numpy as np

"""
Identifies a contiguous horizontal block of a single non-white color in a 1D input grid (row).
Shifts this block 3 positions to the right.
Creates an output grid of the same dimensions, placing the shifted block and filling the rest with the background color (white, 0).
"""

def find_non_background_block(row):
    """
    Finds the first contiguous block of non-background (non-zero) pixels.

    Args:
        row (np.array): A 1D numpy array representing the input row.

    Returns:
        tuple: (color, start_index, length) if a block is found, otherwise None.
               color: The color (int value) of the block.
               start_index: The starting column index of the block.
               length: The length (number of pixels) of the block.
    """
    start_index = -1
    length = 0
    color = 0
    in_block = False

    for i, pixel in enumerate(row):
        if not in_block and pixel != 0:
            # Start of a new block
            in_block = True
            start_index = i
            color = pixel
            length = 1
        elif in_block and pixel == color:
            # Continue the block
            length += 1
        elif in_block and pixel != color:
            # End of the block (hit background or different color)
            # Since we expect only one block, we can stop here.
            break
            
    if start_index != -1:
        return color, start_index, length
    else:
        return None # No block found


def transform(input_grid):
    """
    Transforms the input grid by shifting the non-white block 3 positions right.

    Args:
        input_grid (list or np.array): A 1D list or array representing the input row.

    Returns:
        list: A 1D list representing the transformed output row.
    """
    # Ensure input is a numpy array for easier handling
    input_row = np.array(input_grid)
    grid_length = len(input_row)

    # Initialize output_grid with background color (0)
    output_row = np.zeros(grid_length, dtype=int)

    # 1. Identify the contiguous horizontal block of non-white pixels
    block_info = find_non_background_block(input_row)

    if block_info:
        color, start_index, length = block_info

        # 4. Calculate the new starting column index
        new_start_index = start_index + 3

        # 5. Place the identified block into the output row
        # Ensure the block fits within the grid boundaries
        end_index = new_start_index + length
        if new_start_index < grid_length: # Check if start is within bounds
             # Determine the actual end index considering grid boundary
            actual_end_index = min(end_index, grid_length)
            # Determine how much of the block to actually draw
            draw_length = actual_end_index - new_start_index
            
            # Fill the segment in the output row
            output_row[new_start_index:actual_end_index] = color
            
    # Convert back to list for standard ARC output format if necessary
    # (Although examples show lists of lists, a single row is just a list)
    return output_row.tolist()
