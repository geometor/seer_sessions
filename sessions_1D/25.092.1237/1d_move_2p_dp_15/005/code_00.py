import numpy as np

"""
Transforms a 2D input grid (expected height 1) by:
1. Identifying a contiguous horizontal block of pixels in the first row whose color is neither white (0) nor orange (7) (the 'movable block').
2. Identifying a single orange (7) pixel in the first row (the 'anchor pixel').
3. Creating an output grid of the same dimensions, initialized to white (0).
4. Shifting the 'movable block' 2 columns to the right in the output grid's first row.
5. Placing the 'anchor pixel' in the output grid's first row at its original input column index, potentially overwriting part of the shifted block if they overlap.
"""

def find_movable_block(grid_row):
    """
    Finds the contiguous block of a single color (not 0 or 7) in a given row.

    Args:
        grid_row (np.array): The 1D numpy array representing a single row of the grid.

    Returns:
        tuple: (start_col_index, color, length) of the block, or (None, None, None) if not found.
    """
    start_col_index = -1
    color = -1
    length = 0
    # Iterate through the pixels (columns) in the row
    for i, pixel in enumerate(grid_row):
        # Look for a pixel that is not background (0) and not the anchor (7)
        if pixel != 0 and pixel != 7:
            # If this is the start of a potential block
            if start_col_index == -1:
                start_col_index = i
                color = pixel
                length = 1
            # If this pixel continues the current block
            elif pixel == color:
                length += 1
            # If this pixel starts a *different* non-0/7 block (stop, assuming only one)
            else:
                break
        # If we were tracking a block and hit a 0 or 7, the block has ended
        elif start_col_index != -1:
            break
            
    if start_col_index != -1:
        # Return details of the found block
        return start_col_index, int(color), length # Ensure color is standard int
    else:
        # No suitable block found
        return None, None, None

def find_anchor_pixel(grid_row):
    """
    Finds the column index of the anchor pixel (color 7) in a given row.

    Args:
        grid_row (np.array): The 1D numpy array representing a single row of the grid.

    Returns:
        int: The column index of the anchor pixel, or -1 if not found.
    """
    # Iterate through the pixels (columns) in the row
    for i, pixel in enumerate(grid_row):
        if pixel == 7:
            return i
    # Anchor pixel not found
    return -1

def transform(input_grid):
    """
    Applies the defined transformation rule to the input grid.

    Args:
        input_grid (list): A list of lists of integers representing the input grid.

    Returns:
        list: A list of lists of integers representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output_grid with the same dimensions, filled with white (0)
    output_grid = np.zeros_like(input_np, dtype=int)

    # Assumption: All action happens in the first row (row 0) based on examples
    row_index = 0
    
    # Extract the first row for analysis
    if height > 0:
        first_row = input_np[row_index, :]
    else: # Handle empty input case gracefully
        return output_grid.tolist()

    # Find the movable block in the first row
    block_start_col, block_color, block_length = find_movable_block(first_row)

    # Find the anchor pixel in the first row
    anchor_col = find_anchor_pixel(first_row)

    # Place the shifted movable block in the output grid
    if block_start_col is not None:
        # Calculate the new starting column index for the block (shift right by 2)
        new_block_start_col = block_start_col + 2
        
        # Calculate the end column index (exclusive) for slicing
        # Ensure the block does not go out of the grid's width boundary
        block_end_col = min(new_block_start_col + block_length, width)
        
        # Place the block's color into the output grid's first row at the new position
        # Ensure starting index is within bounds before slicing
        if new_block_start_col < width:
             output_grid[row_index, new_block_start_col:block_end_col] = block_color

    # Place the anchor pixel in the output grid at its original position
    if anchor_col != -1:
        # Ensure anchor index is within bounds (should always be if found)
        if 0 <= anchor_col < width:
            # Place the anchor color (7), potentially overwriting part of the shifted block
            output_grid[row_index, anchor_col] = 7

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()