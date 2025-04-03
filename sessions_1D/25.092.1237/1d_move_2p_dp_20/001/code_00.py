import numpy as np
import copy

"""
Transform a 1D array by moving a contiguous block of a non-background, non-anchor color 
so that its right edge is immediately adjacent to the left of a fixed anchor pixel (gray, 5). 
The space left behind by the moving block and the space it moves over are filled with the 
background color (white, 0). Pixels at and to the right of the anchor pixel remain unchanged.
"""

def find_moving_block(grid_1d, anchor_index):
    """
    Finds the contiguous block of non-white (0) and non-gray (5) pixels 
    to the left of the anchor_index.

    Args:
        grid_1d (np.array): The 1D input grid.
        anchor_index (int): The index of the anchor pixel (5).

    Returns:
        tuple: (block_color, start_index, end_index, length) or (None, -1, -1, 0) if not found.
    """
    block_color = None
    start_index = -1
    end_index = -1
    length = 0

    for i in range(anchor_index):
        pixel = grid_1d[i]
        if pixel != 0 and pixel != 5:
            if block_color is None:  # Start of a potential block
                block_color = pixel
                start_index = i
                end_index = i
                length = 1
            elif pixel == block_color: # Continue the block
                end_index = i
                length += 1
            else: # Different color, shouldn't happen based on examples, but reset if it does
                 block_color = None
                 start_index = -1
                 end_index = -1
                 length = 0
        elif block_color is not None: # End of the block detected by 0 or 5
            # Found the complete block before the anchor
             return block_color, start_index, end_index, length

    # If the loop finished and we were tracking a block
    if block_color is not None:
        return block_color, start_index, end_index, length
        
    # If no block was found before the anchor
    return None, -1, -1, 0


def transform(input_grid):
    """
    Moves a colored block in a 1D array to be adjacent to a gray anchor pixel.

    Args:
        input_grid (list): A 1D list representing the input grid.

    Returns:
        list: A 1D list representing the transformed output grid.
    """
    # Convert input list to numpy array for easier handling
    input_array = np.array(input_grid)
    grid_size = len(input_array)
    
    # Initialize output grid with background color (white, 0)
    output_array = np.zeros(grid_size, dtype=int)

    # Find the anchor pixel (gray, 5)
    anchor_indices = np.where(input_array == 5)[0]
    if len(anchor_indices) == 0:
        # Should not happen based on examples, but handle defensively
        print("Warning: Anchor pixel (5) not found.")
        return input_grid # Or return an empty grid or raise error
    anchor_index = anchor_indices[0] # Assume only one anchor

    # Find the moving block (non-white, non-gray)
    block_color, start_index, end_index, block_length = find_moving_block(input_array, anchor_index)

    if block_color is None:
         # Handle case where no moving block is found (might be valid if input has only 0s and 5s)
         # Copy anchor and everything right of it
         output_array[anchor_index:] = input_array[anchor_index:]
         return output_array.tolist()


    # Copy the anchor pixel and everything to its right from input to output
    output_array[anchor_index:] = input_array[anchor_index:]

    # Calculate the target position for the moving block
    target_end_index = anchor_index - 1
    target_start_index = target_end_index - block_length + 1

    # Place the moving block in the target position in the output grid
    if target_start_index >= 0: # Ensure the block fits
        output_array[target_start_index : target_end_index + 1] = block_color
    else:
        # Handle case where block might not fully fit (shouldn't happen with examples)
        print(f"Warning: Block does not fit entirely to the left of the anchor. Start index {target_start_index}")
        # Place the part that fits
        fit_length = block_length + target_start_index
        if fit_length > 0:
             output_array[0 : fit_length] = block_color


    # The rest of the output grid is already initialized to white (0)

    # Convert numpy array back to list for the expected output format
    return output_array.tolist()