"""
1. Identify the column index of the single green pixel (color 3). Let this be `green_col`.
2. Find the contiguous horizontal block of a single non-white, non-green color located to the left of `green_col`. Identify its color (let's call it `fill_color`) and the column index of its rightmost pixel (let's call it `fill_end_col`).
3. Iterate through the columns from `fill_end_col + 1` up to `green_col - 1`.
4. For each column index in this range, change the pixel's color to `fill_color`.
5. Leave all other pixels unchanged.
"""

import numpy as np

def find_first_occurrence(arr, value):
    """Finds the index of the first occurrence of a value in a 1D numpy array."""
    indices = np.where(arr == value)[0]
    if len(indices) > 0:
        return indices[0]
    return -1 # Indicate not found

def find_last_occurrence(arr, value):
    """Finds the index of the last occurrence of a value in a 1D numpy array."""
    indices = np.where(arr == value)[0]
    if len(indices) > 0:
        return indices[-1]
    return -1 # Indicate not found

def find_colored_block(arr, boundary_col):
    """Finds the fill color and end column of the block left of the boundary."""
    fill_color = -1
    fill_end_col = -1
    for col in range(boundary_col -1, -1, -1): # Iterate backwards from boundary
        pixel_value = arr[col]
        if pixel_value != 0 and pixel_value != 3: # Found a pixel of the block
            fill_color = pixel_value
            # Now find the rightmost extent of this block
            current_col = col
            while current_col < boundary_col and arr[current_col] == fill_color:
                fill_end_col = current_col
                current_col += 1
            break # Found the block, no need to search further left
    return fill_color, fill_end_col


def transform(input_grid):
    """
    Extends a colored block to the right until it reaches a green pixel.

    Args:
        input_grid: A list representing the 1xN input grid.

    Returns:
        A list representing the 1xN output grid.
    """
    # Convert list to numpy array for easier manipulation
    # Assuming input is always a flat list representing a single row
    input_arr = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_arr = input_arr.copy()

    # 1. Find the green pixel (boundary)
    green_col = find_first_occurrence(input_arr, 3)
    if green_col == -1:
        # Should not happen based on examples, but handle defensively
        return output_arr.tolist() 

    # 2. Find the colored block (fill_color and its rightmost edge)
    fill_color = -1
    fill_end_col = -1
    
    # Search for the block to the left of the green pixel
    # Iterate from left up to the green pixel
    for col in range(green_col):
        pixel = input_arr[col]
        # Check if it's a non-white, non-green color
        if pixel != 0 and pixel != 3: 
            fill_color = pixel
            # Find the end of this contiguous block
            current_col = col
            while current_col < green_col and input_arr[current_col] == fill_color:
                 fill_end_col = current_col
                 current_col += 1
            break # Found the first block, assume it's the one we need

    # Check if a valid block was found
    if fill_color == -1 or fill_end_col == -1:
         # Should not happen based on examples
        return output_arr.tolist()

    # 3. & 4. Fill the gap between the block end and the green pixel
    # Iterate from the column *after* the block ends up to *before* the green pixel
    for col_to_fill in range(fill_end_col + 1, green_col):
        output_arr[col_to_fill] = fill_color
        
    # 5. Other pixels remain unchanged (already handled by copying)

    # Convert back to list for the required output format
    return output_arr.tolist()