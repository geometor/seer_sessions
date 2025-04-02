"""
Transforms the input grid by finding a contiguous block of a non-white, non-magenta color,
finding a subsequent single magenta pixel (marker), and filling the gap 
of white pixels between the end of the block and the magenta marker with 
the block's color. Assumes the input is always a single row.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to a single-row input grid.

    Args:
        input_grid: A list containing a single list of integers representing the input row.

    Returns:
        A list containing a single list of integers representing the transformed row.
    """
    
    # Convert input to numpy array for easier handling and modification
    # Assuming input_grid is always [[row_data]]
    grid = np.array(input_grid, dtype=int)
    
    # Ensure it's a single row grid; otherwise return original (or handle error)
    if grid.shape[0] != 1:
        print("Warning: Expected single row grid.")
        return input_grid 
        
    row = grid[0] # Get the actual row data
    height, width = grid.shape
    
    # Initialize variables to store information about the block and marker
    block_color = -1       # Color of the contiguous block
    block_end_index = -1   # Index of the last pixel of the block
    magenta_index = -1     # Index of the magenta marker pixel

    # --- Step 1: Find the contiguous block and its end index ---
    in_block = False
    found_block = False
    for i, pixel in enumerate(row):
        # Detect the start of a block (non-white, non-magenta)
        if not in_block and pixel != 0 and pixel != 6:
            block_color = pixel
            in_block = True
            found_block = True # Mark that we've entered a block at least once
        # Detect the end of the block (pixel changes from block color or end of row)
        elif in_block and pixel != block_color:
            block_end_index = i - 1 # The previous pixel was the end
            in_block = False # Exited the block
            break # Found the block and its end, no need to search further in this loop

    # Handle case where the block extends to the very end of the row
    if in_block: # If loop finished while still 'in_block'
        block_end_index = width - 1

    # If no valid block was found (e.g., all white, or only magenta), return original
    if not found_block or block_color == -1:
        return input_grid

    # --- Step 2: Find the magenta marker after the block ---
    # Start searching from the position *after* the block ends
    search_start_index = block_end_index + 1
    if search_start_index < width: # Only search if there's space after the block
        for i in range(search_start_index, width):
            if row[i] == 6: # Magenta color is 6
                magenta_index = i
                break # Found the first magenta marker after the block

    # If no magenta marker is found after the block, return original
    if magenta_index == -1:
        return input_grid
        
    # --- Step 3: Create the output grid and fill the gap ---
    # Create a copy of the input grid to modify
    output_grid = grid.copy()
    
    # Iterate through the indices between the block end and the magenta marker
    # The range starts one pixel after the block ends and stops *before* the magenta pixel
    fill_start_index = block_end_index + 1
    fill_end_index = magenta_index # The loop goes up to, but not including, this index
    
    for i in range(fill_start_index, fill_end_index):
        # Change the color of pixels in the gap to the block's color
        # Only change if it's currently white (as per observed examples)
        # Although the description implies filling regardless, examples show filling white gaps.
        # Let's stick to the stricter interpretation of filling the gap between block_end and marker.
         output_grid[0, i] = block_color 

    # Convert the numpy array back to a list of lists for the standard ARC format
    return output_grid.tolist()
