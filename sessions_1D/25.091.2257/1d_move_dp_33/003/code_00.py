"""
Move a contiguous colored block within a single-row grid rightwards until its 
right edge is immediately adjacent to the left edge of a fixed orange target 
pixel in the same row.

The input is a 2D grid with exactly one row.
1. Extract the single row from the input grid.
2. Identify the background color (0), the fixed target pixel (7), and the 
   movable colored block (contiguous sequence of non-0, non-7 pixels) within the row.
3. Determine the column index of the target pixel and the color, start index, 
   and length of the movable block.
4. Calculate the destination start column index for the movable block, which is the 
   target pixel's index minus the block's length.
5. Construct the output row:
   a. Initialize a new row with the background color.
   b. Place the movable block at the calculated destination start index.
   c. Place the target pixel at its original index.
   d. Copy any pixels from the input row that were originally to the right of 
      the target pixel.
6. Format the output row as a 2D grid (1xN) and return it.
"""

import numpy as np

def find_target_pixel(row):
    """Finds the column index of the target pixel (7) in a given row."""
    for idx, pixel in enumerate(row):
        if pixel == 7:
            return idx
    # This should not be reached if the assumptions hold true
    raise ValueError("Target pixel (7) not found in the row.") 

def find_movable_block(row):
    """
    Finds the start index, length, and color of the movable block in a row.
    The block consists of contiguous pixels that are not background (0) 
    and not the target (7).
    """
    block_start = -1
    block_color = -1
    block_length = 0
    in_block = False
    
    for idx, pixel in enumerate(row):
        # Check if the pixel belongs to the movable block
        if pixel != 0 and pixel != 7:
            if not in_block:
                # Start of a new block
                block_start = idx
                block_color = pixel
                in_block = True
            block_length += 1
        elif in_block: 
            # End of the block found (encountered 0 or 7, or end of row)
            break # Stop searching once the block is found and passed
             
    if block_start == -1:
         # This should not be reached if the assumptions hold true
        raise ValueError("Movable block not found in the row.")

    return block_start, block_length, block_color


def transform(input_grid):
    """
    Transforms the input grid by moving the colored block next to the target pixel.

    Args:
        input_grid (numpy.ndarray): A 2D NumPy array representing the input grid (shape 1xN).

    Returns:
        numpy.ndarray: A 2D NumPy array representing the transformed output grid (shape 1xN).
    """
    # --- Input Validation and Extraction ---
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid) # Convert if input is list of lists
        
    if input_grid.shape[0] != 1:
        raise ValueError(f"Input grid must have exactly one row, but got shape {input_grid.shape}")
        
    input_row = input_grid[0] # Extract the single row
    row_length = len(input_row)

    # --- Identify Objects ---
    try:
        target_index = find_target_pixel(input_row)
        block_start, block_length, block_color = find_movable_block(input_row)
    except ValueError as e:
        # Handle cases where assumptions might be violated in unexpected inputs
        print(f"Error during object identification: {e}")
        # Return the original grid or handle error appropriately
        return input_grid 

    # --- Calculate Destination ---
    # The block should end at target_index - 1
    # So it should start at (target_index - 1) - (block_length - 1) = target_index - block_length
    destination_start_index = target_index - block_length
    
    # --- Construct Output Row ---
    # Initialize output row with background color (0)
    output_row = [0] * row_length

    # Place the Movable Block at its new position
    # Ensure indices are within bounds (though assumptions imply they should be)
    start = max(0, destination_start_index)
    end = min(row_length, destination_start_index + block_length)
    for i in range(start, end):
        output_row[i] = block_color

    # Place the Target Pixel at its original position
    if 0 <= target_index < row_length: # Boundary check
        output_row[target_index] = 7

    # Copy pixels from the input that were originally to the right of the Target Pixel
    # Start copying from the position right after the target pixel
    copy_start_index = target_index + 1
    if copy_start_index < row_length:
        for i in range(copy_start_index, row_length):
             output_row[i] = input_row[i]

    # --- Format Output ---
    # Convert the output row list back to a 2D numpy array (1xN)
    output_grid = np.array([output_row])

    return output_grid