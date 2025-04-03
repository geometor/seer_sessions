```python
"""
Shift a contiguous block of non-white, non-azure pixels 2 positions to the right, 
while keeping a single azure (8) pixel fixed in its original position. The 
background is filled with white (0).
"""

import numpy as np

def find_first_pixel(grid_row, color):
    """Finds the index of the first occurrence of a specific color in a 1D list."""
    try:
        return grid_row.index(color)
    except ValueError:
        return -1 # Not found

def find_contiguous_block(grid_row, excluded_colors):
    """
    Finds the first contiguous block of pixels not matching the excluded colors.
    Returns the start index, length, and color of the block, or None if not found.
    """
    start_index = -1
    block_color = -1
    in_block = False
    for i, pixel in enumerate(grid_row):
        if pixel not in excluded_colors:
            if not in_block:
                # Start of a new block
                start_index = i
                block_color = pixel
                in_block = True
        elif in_block:
            # End of the block
            length = i - start_index
            return start_index, length, block_color
    # Check if the block extends to the end of the row
    if in_block:
        length = len(grid_row) - start_index
        return start_index, length, block_color
    return None # No block found

def transform(input_grid):
    """
    Transforms the input grid according to the rule: shift the main colored block
    right by 2 positions, keeping the azure pixel fixed.
    """
    # Assuming input is a list containing one row (list)
    input_row = input_grid[0]
    grid_width = len(input_row)

    # 1. Initialize the output grid with white (0) pixels.
    output_row = [0] * grid_width

    # 2. Locate the position of the single azure (8) pixel.
    azure_pos = find_first_pixel(input_row, 8)

    # 3. Place an azure (8) pixel at the same position in the output grid.
    if azure_pos != -1:
        output_row[azure_pos] = 8

    # 4. Identify the contiguous block (not white 0, not azure 8).
    block_info = find_contiguous_block(input_row, excluded_colors={0, 8})

    if block_info:
        start_index, length, color = block_info

        # 5. Calculate the new starting position for this block (shift right by 2).
        new_start_index = start_index + 2

        # 6. Place this contiguous block into the output grid at the new position.
        # Ensure we don't write past the grid boundary or over the azure pixel
        for i in range(length):
            current_output_index = new_start_index + i
            # Check grid bounds
            if 0 <= current_output_index < grid_width:
                 # Only overwrite if the target cell isn't the fixed azure pixel
                 # (In this specific task, the block and azure pixel seem separate,
                 # but this check adds robustness)
                 if output_row[current_output_index] != 8:
                     output_row[current_output_index] = color
            # If out of bounds, stop placing the rest of the block
            else:
                 break

    # Return the output grid in the required list-of-lists format
    return [output_row]

```