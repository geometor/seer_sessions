import numpy as np

"""
Rearranges elements in a 1D grid. It identifies a single magenta pixel (6) 
and a single contiguous block of another color (neither white 0 nor magenta 6). 
The transformation moves the colored block so its rightmost pixel is positioned 
immediately to the left of the magenta pixel's original location. The rest of 
the grid is filled with white (0) pixels.
"""

def find_magenta_pixel(grid_row):
    """
    Finds the index of the first magenta (6) pixel in the row.

    Args:
        grid_row: A list or numpy array representing the grid row.

    Returns:
        The index of the magenta pixel, or -1 if not found.
    """
    for idx, pixel in enumerate(grid_row):
        if pixel == 6:
            return idx
    return -1 # Indicates magenta pixel not found

def find_colored_block(grid_row):
    """
    Finds the first contiguous block of non-white (0), non-magenta (6) pixels.

    Args:
        grid_row: A list or numpy array representing the grid row.

    Returns:
        A tuple (color, start_index, length) of the block.
        Returns (-1, -1, 0) if no such block is found.
    """
    block_color = -1
    block_start = -1
    block_length = 0
    in_block = False
    
    for idx, pixel in enumerate(grid_row):
        # Check if the current pixel could be part of the colored block
        is_block_pixel = (pixel != 0 and pixel != 6)
        
        if is_block_pixel:
            if not in_block:
                # Start of a new potential block
                block_color = pixel
                block_start = idx
                block_length = 1
                in_block = True
            elif pixel == block_color:
                 # Continue the existing block (same color)
                 block_length += 1
            else:
                 # Found a different color block, stop searching 
                 # (task assumes only one relevant block needs processing)
                 break 
        elif in_block:
            # End of the block (hit 0 or 6 after being in a block)
            break
            
    # If the loop finishes while still in_block, the block extends to the end
    # The values captured (block_color, block_start, block_length) are correct.
    
    # Ensure block_start is valid if length > 0
    if block_length > 0 and block_start == -1:
        # This state should not be reachable with the logic above, but as a safeguard:
        print("Warning: Inconsistent block state detected.")
        return -1, -1, 0 # Indicate error/no valid block found
        
    return block_color, block_start, block_length

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid (expected 1xN).

    Returns:
        A list of lists representing the transformed grid.
    """
    # Validate input grid format
    if not input_grid or not isinstance(input_grid, list) or not input_grid[0] or not isinstance(input_grid[0], list):
        print("Warning: Invalid input grid format.")
        return [] 
        
    # Extract the first (and assumed only) row
    input_row = np.array(input_grid[0])
    grid_width = len(input_row)
    
    # Initialize the output grid (row) with white pixels (0)
    output_row = np.zeros(grid_width, dtype=int)

    # --- Step 1 & 2: Identify Elements ---
    # Find the index of the magenta (6) marker pixel
    marker_index = find_magenta_pixel(input_row)
    if marker_index == -1:
         print("Warning: Magenta pixel (6) not found. Returning grid of zeros.")
         # Returning grid of zeros as per construction method, marker is required.
         return [output_row.tolist()] 

    # Find the color, start index, and length of the colored block
    # Note: original_start_index is not needed for constructing the output directly
    block_color, _, block_length = find_colored_block(input_row) 
    if block_color == -1 or block_length <= 0:
        print("Warning: Colored block not found or has zero length. Placing only marker.")
        # Place only the marker if block is missing, then return
        output_row[marker_index] = 6
        return [output_row.tolist()]

    # --- Step 3 & 4: Construct Output ---
    # Place the marker pixel in the output grid
    output_row[marker_index] = 6

    # Calculate the target starting index for the colored block
    new_start_index = marker_index - block_length

    # Place the colored block at its new position, performing boundary checks
    if new_start_index >= 0:
        new_end_index = new_start_index + block_length
        # Ensure the placement fits entirely within the grid
        if new_end_index <= grid_width:
             # Place the block using its color and calculated position
             output_row[new_start_index : new_end_index] = block_color
        else:
             # This case shouldn't occur based on training examples, but log if it does
             print(f"Warning: Calculated block placement [{new_start_index}:{new_end_index}] exceeds grid width {grid_width}. Block not placed correctly.")
             # Decide behavior: Place partially? Place nothing? Current logic places nothing if out of bounds.
             # Let's refine to place what fits, similar to previous attempt's logic:
             safe_end_index = min(new_end_index, grid_width)
             if new_start_index < safe_end_index:
                 output_row[new_start_index : safe_end_index] = block_color
             
    else:
         # Handle cases where the calculated start index is negative (block too long)
         print(f"Warning: Calculated new_start_index ({new_start_index}) is negative. Placing partially if possible.")
         # Place the part of the block that fits starting from index 0
         place_length = block_length + new_start_index # e.g., start=-1, len=3 -> place_len=2
         if place_length > 0:
              # Ensure place_length doesn't exceed grid width (e.g., tiny grid)
              place_length = min(place_length, grid_width) 
              output_row[0 : place_length] = block_color

    # --- Step 5: Return Result ---
    # Return the modified row wrapped in a list
    return [output_row.tolist()]