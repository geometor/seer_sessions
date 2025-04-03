import copy

"""
Identifies the single contiguous horizontal block of non-white pixels in the 1D input grid.
Shifts this block one position to the right.
The pixel at the original start position of the block becomes white.
The pixel immediately to the right of the original end position of the block takes the block's color, 
provided this position is within the grid bounds.
"""

def find_non_white_block(grid):
    """
    Finds the first contiguous block of a non-white color in a 1D grid.

    Args:
        grid: A list of integers representing the 1D grid.

    Returns:
        A tuple (color, start_index, end_index) if a block is found,
        otherwise (None, -1, -1).
    """
    start_index = -1
    end_index = -1
    block_color = None

    for i, pixel in enumerate(grid):
        if pixel != 0:  # Found the start of a potential block
            if start_index == -1: # Only capture the first block encountered
                start_index = i
                block_color = pixel
                # Continue searching for the end of this specific block
                for j in range(i, len(grid)):
                    if grid[j] == block_color:
                        end_index = j
                    else:
                        # End of the block found (or different color)
                        break
                # Since we only care about the first block, we can break after finding it
                break # Exit the outer loop once the first block is fully identified

    return block_color, start_index, end_index

def transform(input_grid):
    """
    Shifts the single non-white block in the input grid one step to the right.

    Args:
        input_grid: A list of integers representing the 1D input grid.

    Returns:
        A list of integers representing the transformed 1D output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = list(input_grid) # Ensure it's a mutable list copy
    grid_width = len(output_grid)

    # Find the non-white block
    block_color, start_index, end_index = find_non_white_block(input_grid)

    # If a block was found, perform the shift
    if block_color is not None:
        # Set the original start position to white
        if start_index >= 0: # Check if start_index is valid
             output_grid[start_index] = 0

        # Set the position to the right of the original end position to the block color, if within bounds
        new_end_pos = end_index + 1
        if new_end_pos < grid_width:
            output_grid[new_end_pos] = block_color

    # Return the modified grid
    return output_grid