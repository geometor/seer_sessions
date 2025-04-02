"""
Transforms a 1D grid by finding a contiguous block of a non-white, non-green color 
and extending it to the right, filling the gap with its color until it reaches 
a single green pixel which acts as a boundary.

1. Create a copy of the input row to serve as the output row.
2. Locate the column index of the single green pixel (color 3) in the input row. 
   Let this be `green_col`.
3. Scan the input row from left to right, up to (but not including) `green_col`, 
   to find the *first* contiguous block of pixels with a color that is neither 
   white (0) nor green (3).
4. Identify the color of this block (`fill_color`) and the column index of its 
   rightmost pixel (`fill_end_col`).
5. If such a block is found:
   a. Iterate through the columns from `fill_end_col + 1` up to `green_col - 1`.
   b. For each column index in this range, set the corresponding pixel in the 
      *output* row to `fill_color`.
6. Return the modified output row.
"""

import numpy as np

def find_first_of(arr, values):
    """Finds the index of the first occurrence of any value in `values` within `arr`."""
    for val in values:
        indices = np.where(arr == val)[0]
        if len(indices) > 0:
            return indices[0]
    return -1 # Not found

def find_block_left_of(arr, boundary_col):
    """
    Finds the fill color and end column index of the first non-white, non-green block
    occurring before the specified boundary column.
    """
    fill_color = -1
    fill_end_col = -1
    
    for col in range(boundary_col):
        pixel_value = arr[col]
        # Check if it's a potential start of the block (non-white, non-green)
        if pixel_value != 0 and pixel_value != 3:
            fill_color = pixel_value
            # Find the end of this contiguous block
            current_col = col
            # Continue as long as we are before the boundary and the color matches
            while current_col < boundary_col and arr[current_col] == fill_color:
                fill_end_col = current_col
                current_col += 1
            # Found the first block and its end, no need to search further
            break 
            
    return fill_color, fill_end_col

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
        # Green pixel not found, return the original grid (as per current understanding)
        return output_arr.tolist() 
    green_col = green_indices[0] # Assume only one green pixel as per examples

    # 3. & 4. Find the fill block's color and its rightmost extent.
    fill_color, fill_end_col = find_block_left_of(input_arr, green_col)

    # 5. If a valid block was found, fill the gap.
    if fill_color != -1 and fill_end_col != -1:
        # Iterate from the column *after* the block ends up to *before* the green pixel
        start_fill_col = fill_end_col + 1
        end_fill_col = green_col # The loop range is exclusive of the end value
        
        for col_to_fill in range(start_fill_col, end_fill_col):
            # Check if the pixel to fill is currently white (optional, but matches examples)
            # if output_arr[col_to_fill] == 0: 
            output_arr[col_to_fill] = fill_color
            
    # 6. Return the modified output row as a list.
    return output_arr.tolist()