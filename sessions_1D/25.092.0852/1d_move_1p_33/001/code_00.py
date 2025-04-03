"""
Identifies a single contiguous block of a non-white color in a 1D input grid.
Shifts this block exactly one position to the right.
The shift is achieved by changing the leftmost pixel of the original block to white (0)
and changing the white pixel immediately to the right of the block's original position 
to the block's color. The block's color and length are preserved.
"""

import numpy as np

def find_block(grid_row):
    """
    Finds the start index, end index, and color of the first contiguous
    non-zero block in a 1D numpy array.
    """
    start_index = -1
    end_index = -1
    block_color = 0
    in_block = False

    for i, pixel in enumerate(grid_row):
        if pixel != 0 and not in_block:
            start_index = i
            block_color = pixel
            in_block = True
        elif pixel == 0 and in_block:
            end_index = i - 1
            break # Found the end of the block

    # Handle case where block goes to the end of the grid
    if in_block and end_index == -1:
        end_index = len(grid_row) - 1
        
    if start_index == -1: # No block found
        return None, None, None

    return start_index, end_index, block_color

def transform(input_grid):
    """
    Shifts a contiguous block of color one position to the right in a 1D grid.

    Args:
        input_grid (list of lists): A 2D list representing the input grid. 
                                     Expected to contain only one row.

    Returns:
        list of lists: A 2D list representing the transformed grid.
    """
    # Ensure input is treated as a 1D array for processing
    # Assuming the relevant data is always in the first row
    if not input_grid:
        return []
    input_row = np.array(input_grid[0], dtype=int)

    # Create a copy to modify for the output
    output_row = input_row.copy()

    # Find the contiguous block of non-white pixels
    start_index, end_index, block_color = find_block(input_row)

    # Check if a block was found and if the shift is possible
    if start_index is not None and end_index is not None and block_color != 0:
        # Ensure the block is not already at the very right edge
        if end_index + 1 < len(output_row):
            # Change the leftmost pixel of the original block position to white
            output_row[start_index] = 0
            # Change the pixel to the right of the original block's end to the block's color
            output_row[end_index + 1] = block_color
        # Else: If the block is at the right edge, no shift occurs (or handle specific edge case if needed)
        # Based on examples, it seems valid shifts only happen if space exists.

    # Convert the modified numpy array back to the list of lists format
    output_grid = [output_row.tolist()]
    
    return output_grid
