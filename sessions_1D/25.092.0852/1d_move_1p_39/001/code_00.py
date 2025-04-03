"""
Identifies a contiguous block of non-white pixels in a 1D input array and shifts this block one position to the right in the output array, maintaining the background color (white) and the array size.
"""

import numpy as np

def find_non_white_block(grid_1d):
    """
    Finds the first contiguous block of non-white pixels in a 1D array.

    Args:
        grid_1d: A 1D list or numpy array.

    Returns:
        A tuple (color, start_index, end_index) if a block is found,
        otherwise (None, -1, -1).
        - color: The color of the non-white block.
        - start_index: The starting index of the block.
        - end_index: The ending index (inclusive) of the block.
    """
    start_index = -1
    end_index = -1
    block_color = None

    for i, pixel in enumerate(grid_1d):
        if pixel != 0:  # Found a non-white pixel
            if start_index == -1: # Found the start of a potential block
                start_index = i
                block_color = pixel
            # Check if the current pixel continues the block
            elif pixel == block_color:
                 # This condition assumes blocks are contiguous. If we find a pixel
                 # of the same color after a break, it's considered a new block.
                 # In this specific task's examples, there's only one block.
                 pass # Continue the block
            else: # Found a different non-white color, ending the first block
                 end_index = i - 1
                 break
        elif start_index != -1: # Found a white pixel after a block started
            end_index = i - 1
            break

    # If the loop finished and a block started but didn't end (block goes to the end)
    if start_index != -1 and end_index == -1:
        end_index = len(grid_1d) - 1
        # Re-verify the last pixel actually belongs to the block
        if grid_1d[end_index] != block_color:
             # This case shouldn't happen with contiguous blocks ending at the edge
             # but added for robustness. If the last pixel wasn't part of the block,
             # adjust the end index. Example: [6, 6, 0] -> start=0, end needs to be 1.
             end_index = len(grid_1d) - 2 # Adjust if last pixel wasn't part of the block


    # Final check to ensure the end_index isn't before the start_index
    # This can happen if only one non-white pixel exists, e.g. [0, 6, 0]
    if start_index != -1 and end_index < start_index:
         end_index = start_index # A block of size 1


    return block_color, start_index, end_index


def transform(input_grid):
    """
    Shifts the first contiguous non-white block in a 1D input grid one position to the right.

    Args:
        input_grid: A list representing the 1D input grid.

    Returns:
        A list representing the 1D output grid with the block shifted.
    """
    # Convert input to numpy array for easier handling if needed, though list is fine
    grid_array = np.array(input_grid)
    grid_size = len(grid_array)

    # Find the non-white block
    block_color, start_index, end_index = find_non_white_block(grid_array)

    # Initialize output_grid with background color (white)
    output_grid = np.zeros(grid_size, dtype=int) # Default is 0 (white)

    # If a block was found, shift it
    if block_color is not None:
        # Calculate new position
        new_start_index = start_index + 1
        new_end_index = end_index + 1
        block_length = end_index - start_index + 1

        # Check if the new position is within bounds
        if new_end_index < grid_size:
             # Copy the block to the new position in the output grid
             output_grid[new_start_index : new_end_index + 1] = block_color
        # Handle cases where the block might partially shift off the edge
        # Based on examples, it seems we only need to copy the part that fits.
        elif new_start_index < grid_size:
             num_pixels_to_copy = grid_size - new_start_index
             output_grid[new_start_index : grid_size] = block_color


    # Convert back to list for the expected output format
    return output_grid.tolist()