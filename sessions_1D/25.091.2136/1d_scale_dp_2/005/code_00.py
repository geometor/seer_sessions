"""
Transforms a 1D grid (represented as a list) by finding the first contiguous block 
of a non-white (0), non-green (3) color located to the left of a single green (3) 
pixel. This block's color is then used to fill the gap (initially white pixels) 
between the end of the block and the green pixel. Pixels to the left of the block, 
the green pixel itself, and pixels to its right remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the fill transformation to the input grid.

    Args:
        input_grid: A list representing the 1xN input grid.

    Returns:
        A list representing the transformed 1xN output grid.
    """
    # Convert list to numpy array for efficient operations
    input_arr = np.array(input_grid, dtype=int)
    
    # 1. Create a copy of the input row to serve as the output row.
    output_arr = input_arr.copy()

    # 2. Locate the column index of the single green pixel (color 3).
    green_indices = np.where(input_arr == 3)[0]
    if len(green_indices) == 0:
        # If no green pixel is found, return the unmodified copy.
        return output_arr.tolist() 
    green_col = green_indices[0] # Assume only one green pixel as per examples

    # Initialize variables to find the fill block
    fill_color = -1
    fill_block_end_col = -1
    found_block = False

    # 3. Scan the input row from left up to green_col to find the first non-white, non-green pixel.
    for col in range(green_col):
        pixel_value = input_arr[col]
        # Check if it's a potential start of the block (non-white, non-green)
        if pixel_value != 0 and pixel_value != 3:
            # 4a. Identify its color as fill_color.
            fill_color = pixel_value
            
            # 4b. Determine the rightmost extent of the contiguous block.
            current_col = col
            # Continue as long as we are before the boundary and the color matches
            while current_col < green_col and input_arr[current_col] == fill_color:
                fill_block_end_col = current_col
                current_col += 1
                
            # Found the first block and its end, no need to search further
            found_block = True
            break 
            
    # 5. If no non-white, non-green pixel is found before green_col, block not found.
    # (Handled by found_block flag)

    # If a valid block was found, proceed to fill the gap.
    if found_block:
        # 4c. Iterate through the columns from fill_block_end_col + 1 up to green_col - 1.
        start_fill_col = fill_block_end_col + 1
        # The loop range's end is exclusive, so green_col works directly.
        end_fill_col_exclusive = green_col 
        
        for col_to_fill in range(start_fill_col, end_fill_col_exclusive):
            # 4d. Set the color of the pixel in the output row to fill_color.
            # Note: We overwrite whatever is there (usually white, based on examples)
            output_arr[col_to_fill] = fill_color
            
    # 6. Return the modified output row as a list.
    return output_arr.tolist()