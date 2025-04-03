import numpy as np

"""
Transforms a 1D input grid by:
1. Identifying a contiguous block of pixels whose color is neither white (0) nor orange (7) (the 'movable block').
2. Identifying a single orange (7) pixel (the 'anchor pixel').
3. Creating an output grid of the same size, initialized to white (0).
4. Shifting the 'movable block' 2 positions to the right in the output grid.
5. Placing the 'anchor pixel' in the output grid at its original input position, potentially overwriting part of the shifted block if they overlap.
"""

def find_movable_block(grid):
    """
    Finds the contiguous block of a single color (not 0 or 7).

    Args:
        grid (np.array): The 1D input grid.

    Returns:
        tuple: (start_index, color, length) of the block, or (None, None, None) if not found.
    """
    start_index = -1
    color = -1
    length = 0
    for i, pixel in enumerate(grid):
        # Look for a pixel that is not background (0) and not the anchor (7)
        if pixel != 0 and pixel != 7:
            # If this is the start of a potential block
            if start_index == -1:
                start_index = i
                color = pixel
                length = 1
            # If this pixel continues the current block
            elif pixel == color:
                length += 1
            # If this pixel starts a *different* non-0/7 block (should not happen per constraints)
            else:
                break # Stop searching as the block ended unexpectedly
        # If we were tracking a block and hit a 0 or 7, the block has ended
        elif start_index != -1:
            break
            
    if start_index != -1:
        # Return details of the found block
        return start_index, int(color), length # Ensure color is standard int
    else:
        # No suitable block found
        return None, None, None

def find_anchor_pixel(grid):
    """
    Finds the index of the anchor pixel (color 7).

    Args:
        grid (np.array): The 1D input grid.

    Returns:
        int: The index of the anchor pixel, or -1 if not found.
    """
    for i, pixel in enumerate(grid):
        if pixel == 7:
            return i
    # Anchor pixel not found (should not happen per constraints)
    return -1

def transform(input_grid):
    """
    Applies the defined transformation rule to the input grid.

    Args:
        input_grid (list): A list of integers representing the input grid.

    Returns:
        list: A list of integers representing the transformed output grid.
    """
    # Convert input list to numpy array for easier processing
    input_np = np.array(input_grid)
    grid_size = len(input_np)

    # Initialize output_grid with white (0)
    output_grid = np.zeros(grid_size, dtype=int)

    # Step 1 & 2: Identify the movable block and anchor pixel
    block_start, block_color, block_length = find_movable_block(input_np)
    anchor_index = find_anchor_pixel(input_np)

    # Step 4 & 5: Calculate new position and place the movable block
    if block_start is not None:
        new_block_start = block_start + 2
        
        # Ensure the block doesn't start or go out of bounds
        if new_block_start < grid_size:
            end_index = min(new_block_start + block_length, grid_size)
            # Place the block using slicing
            output_grid[new_block_start:end_index] = block_color

    # Step 6: Place the anchor pixel, potentially overwriting the block
    if anchor_index != -1:
        # Ensure anchor index is within bounds (should always be)
        if 0 <= anchor_index < grid_size:
            output_grid[anchor_index] = 7

    # Convert numpy array back to list for the expected output format
    return output_grid.tolist()