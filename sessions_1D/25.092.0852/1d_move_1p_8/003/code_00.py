"""
Identifies a single contiguous horizontal block of non-white pixels in the 
input grid (which has shape 1xN) and shifts this block one position to the 
right. The block's color and length are preserved. The background remains 
white (0), and the grid dimensions are unchanged.
"""

import numpy as np

def find_block_in_row(row):
    """
    Finds the first contiguous block of non-white pixels in a 1D numpy array (row).

    Args:
        row: A 1D numpy array representing the grid row.

    Returns:
        A tuple (start_index, end_index, color) if a block is found,
        otherwise returns (-1, -1, -1).
    """
    start_index = -1
    end_index = -1
    color = -1
    in_block = False
    
    for i, pixel in enumerate(row):
        # Start of a block
        if pixel != 0 and not in_block:
            start_index = i
            color = pixel
            in_block = True
        # End of a block (transition to white)
        elif pixel == 0 and in_block:
            end_index = i - 1
            break  # Found the end, stop searching
            
    # Handle case where block extends to the very end of the row
    if in_block and end_index == -1:
        end_index = len(row) - 1

    # Verify block integrity (optional, based on problem constraints)
    # Ensures only one color within the detected bounds
    if start_index != -1:
        block_slice = row[start_index : end_index + 1]
        if not np.all(block_slice == color):
            # This condition implies multiple colors or gaps within what was initially
            # detected as a single block's start/end. Given the simple examples,
            # this might indicate an issue or a more complex scenario not covered.
            # For this specific task, we assume blocks are single-colored and contiguous.
             print(f"Warning: Inconsistent block found. Start={start_index}, End={end_index}, Expected Color={color}, Slice={block_slice}")
             # Depending on interpretation, might need refinement. Sticking to simple shift for now.
             pass # Proceed with the found indices/color for the simple case

    if start_index == -1: # No block found at all
        return -1, -1, -1
        
    return start_index, end_index, color

def transform(input_grid):
    """
    Shifts a horizontal block of color one step to the right within a 1xN grid.

    Args:
        input_grid: A 2D numpy array representing the input grid (expected shape 1xN).

    Returns:
        A 2D numpy array representing the output grid with the block shifted.
    """
    # Ensure input is a numpy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)

    # Validate input shape (optional but good practice)
    if input_grid.shape[0] != 1:
        raise ValueError("Input grid must have exactly one row.")

    # Extract the single row
    input_row = input_grid[0]
    grid_width = len(input_row)

    # Find the non-white block in the input row
    start_index, end_index, color = find_block_in_row(input_row)

    # Initialize the output row with background color (white)
    output_row = np.zeros(grid_width, dtype=input_row.dtype)

    # If a block was found, shift it
    if start_index != -1:
        block_length = end_index - start_index + 1
        
        # Calculate the new starting position (shifted one unit right)
        new_start_index = start_index + 1
        new_end_index = new_start_index + block_length - 1 # Calculate new end index

        # Check if the shifted block fits within the grid boundaries
        if new_end_index < grid_width:
            # Place the block into the new grid at the shifted position
            output_row[new_start_index : new_end_index + 1] = color
        else:
            # Handle cases where the block shifts partially or fully off the grid.
            # Based on examples, this shouldn't happen, but defensive coding is good.
            # If it shifts partially off, copy the part that fits.
            placeable_length = grid_width - new_start_index
            if placeable_length > 0:
                 output_row[new_start_index : new_start_index + placeable_length] = color
            # If new_start_index itself is out of bounds, the row remains all zeros.
            # print(f"Warning: Shifted block exceeds grid boundary. Original: ({start_index}-{end_index}), New Start: {new_start_index}")


    # Reshape the output row back to a 2D grid (1xN)
    output_grid = output_row.reshape(1, grid_width)
    
    return output_grid