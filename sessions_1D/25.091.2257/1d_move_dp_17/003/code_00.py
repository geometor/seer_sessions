import numpy as np

"""
Transforms a 1D input grid by moving a contiguous block of non-background (0), 
non-anchor (8) color pixels so that its right end is positioned immediately 
to the left of a fixed anchor pixel (azure/8). The background, anchor pixel, 
and the properties (color, length) of the movable block are preserved.
"""

def find_movable_block(input_array):
    """
    Finds the first contiguous block of color that is not background (0) or anchor (8).
    
    Args:
        input_array: A 1D numpy array representing the input grid.

    Returns:
        A tuple (block_color, block_length):
        - block_color: The integer color code of the block found.
        - block_length: The length of the block found.
        Returns (None, 0) if no such block is found.
    """
    block_color = None
    block_length = 0
    in_block = False

    for i, pixel in enumerate(input_array):
        is_movable_color = (pixel != 0 and pixel != 8)

        if not in_block and is_movable_color:
            # Start of a new block
            in_block = True
            block_color = pixel
            block_length = 1
        elif in_block:
            if pixel == block_color:
                # Continue the current block
                block_length += 1
            else:
                # End of the block (hit 0, 8, or different color)
                break # Since we only care about the first block
                
    return block_color, block_length

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list or list-of-lists representing the potentially 1xN input grid.

    Returns:
        A list representing the transformed 1D output grid.
    """
    # 1. Ensure input is treated as a 1D array
    input_array = np.array(input_grid, dtype=int).flatten()
    grid_width = len(input_array)

    # 2. Create output grid filled with background color (0)
    output_grid = np.zeros(grid_width, dtype=int)

    # 3. Find the anchor pixel (azure/8)
    anchor_indices = np.where(input_array == 8)[0]
    if len(anchor_indices) == 0:
        # Handle error: anchor pixel not found (though examples imply it's always there)
        # Returning the initialized grid might be a fallback.
        print("Warning: Anchor pixel (8) not found.")
        return output_grid.tolist() 
    anchor_index = anchor_indices[0] # Assume only one anchor

    # Place the anchor in the output grid
    output_grid[anchor_index] = 8

    # 4. Find the contiguous movable block (non-0, non-8)
    block_color, block_length = find_movable_block(input_array)

    # If no movable block was found, just return the grid with the anchor
    if block_color is None:
        return output_grid.tolist()

    # 5. Calculate the target end index for the block
    target_end_index = anchor_index - 1

    # 6. Calculate the target start index for the block
    target_start_index = target_end_index - block_length + 1

    # 7. Place the block at the target position in the output grid
    # Basic check to ensure target indices are plausible before slicing
    if target_start_index >= 0 and target_end_index < grid_width:
        output_grid[target_start_index : target_end_index + 1] = block_color
    else:
        # Handle cases where the calculated position is out of bounds.
        # Based on training examples, this might not occur, but it's safer to log.
        # A simple approach is to not place the block if it doesn't fully fit.
        print(f"Warning: Calculated block position [{target_start_index}, {target_end_index}] is out of grid bounds [0, {grid_width-1}]. Block not placed.")


    # 8. Return the result as a standard Python list
    return output_grid.tolist()