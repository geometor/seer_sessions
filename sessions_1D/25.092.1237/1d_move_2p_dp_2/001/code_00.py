import numpy as np

"""
Shift a contiguous colored block (non-white, non-red) two positions to the right, 
keeping a single red pixel stationary. The grid is assumed to be 1D (a single row).
"""

def find_colored_block(row):
    """Finds the start index, end index, and color of the colored block."""
    start_index = -1
    end_index = -1
    block_color = -1
    for i, pixel in enumerate(row):
        if pixel != 0 and pixel != 2: # Found a potential start or part of the block
            if start_index == -1:
                start_index = i
                block_color = pixel
            # Check if the current pixel continues the block
            if i + 1 < len(row) and row[i+1] == block_color:
                continue # Continue scanning the block
            else: # End of the block found
                end_index = i
                return start_index, end_index, block_color
    return None # Should not happen based on examples

def find_pixel(row, color):
    """Finds the index of the first pixel with the specified color."""
    for i, pixel in enumerate(row):
        if pixel == color:
            return i
    return -1 # Should not happen based on examples

def transform(input_grid):
    """
    Transforms the input grid by shifting the colored block two steps to the right,
    keeping the red pixel stationary.
    """
    # As grids are 1xN, extract the single row
    input_row = input_grid[0]
    height = 1
    width = len(input_row)

    # Initialize output_grid with background color (white)
    output_row = [0] * width

    # 1. Locate the contiguous block of pixels (not white or red)
    block_start, block_end, block_color = find_colored_block(input_row)

    # 2. Locate the single red pixel (2)
    red_pixel_index = find_pixel(input_row, 2)

    # 3. Create a new output grid (row) initialized to white
    #    (Already done above)

    # 4. Place the red pixel (2) into the output grid at its original index
    if red_pixel_index != -1:
        output_row[red_pixel_index] = 2

    # 5. Calculate the new starting index for the colored block
    new_block_start = block_start + 2

    # 6. Calculate the new ending index for the colored block
    new_block_end = block_end + 2

    # 7. Fill the pixels in the output grid for the shifted block
    #    Ensure indices are within bounds (although not strictly necessary based on examples)
    for i in range(new_block_start, new_block_end + 1):
         if 0 <= i < width: # Basic bounds check
            output_row[i] = block_color

    # Wrap the row back into the grid format
    output_grid = [output_row]

    return output_grid
