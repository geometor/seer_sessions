"""
Shift a single contiguous block of non-white pixels found in a 1xN input grid one position to the right.

1. Receive the input as a 2D grid (1 row, N columns).
2. Extract the first row.
3. Identify the contiguous block of non-white pixels in this row, noting its color (C), start column (start_col), and end column (end_col).
4. Create an output grid as a copy of the input grid.
5. Modify the first row of the output grid: set pixel at start_col to white (0), set pixel at end_col + 1 to color C.
6. Return the modified output grid.
"""

import numpy as np

def find_non_white_block_in_row(row):
    """
    Finds the start index, end index, and color of the first contiguous non-white block in a 1D array.

    Args:
        row (np.array): A 1D numpy array representing a row of pixels.

    Returns:
        tuple: (start_index, end_index, color) or (-1, -1, 0) if no block is found.
    """
    start_index = -1
    end_index = -1
    color = 0
    for i, pixel in enumerate(row):
        if pixel != 0:  # Non-white pixel found
            if start_index == -1:  # Start of a new block
                start_index = i
                color = pixel
            end_index = i  # Update end index as long as the block continues
        elif start_index != -1:  # End of the block (pixel is white, and we were in a block)
            break  # Found the first block, stop searching
            
    # Handle case where the block extends to the very end of the row
    # (The loop finishes before hitting a white pixel after the block)
    # The end_index will be correctly set in this case by the loop.

    return start_index, end_index, color

def transform(input_grid):
    """
    Transforms the input grid by shifting the non-white block in the first row one step to the right.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid (expected 1xN).

    Returns:
        list[list[int]]: A 2D list representing the transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Check if the input grid has at least one row
    if input_np.shape[0] == 0:
        return input_grid # Return original if empty

    # Initialize output_grid as a copy of the input
    output_np = input_np.copy()

    # Extract the first row (assuming the relevant data is always in the first row based on examples)
    # If the grid could have more rows and the transformation only applies to the first, this is correct.
    # If the block could be in another row, logic would need adjustment.
    row_to_process = output_np[0] 
    
    # Find the non-white block in this row
    start_col, end_col, color = find_non_white_block_in_row(row_to_process)

    # Check if a block was found
    if start_col != -1:
        # Ensure the shift is possible (check bounds)
        new_end_col = end_col + 1
        row_width = output_np.shape[1]

        # Change the original start position to white in the first row of the output
        output_np[0, start_col] = 0
        
        # Change the pixel to the right of the original block's end to the block's color, if within bounds
        if new_end_col < row_width:
            output_np[0, new_end_col] = color
        # If new_end_col is out of bounds, the rightmost part of the block effectively "falls off" the grid.
        # This is handled implicitly as we only modify within bounds. The original pixel at new_end_col (if it existed) is not modified to color.

    # Convert the result back to a list of lists
    return output_np.tolist()