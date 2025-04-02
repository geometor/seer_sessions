import numpy as np

"""
Identifies a single contiguous block of non-white pixels in the single row 
of the input 2D grid and shifts this block 3 positions (columns) to the right 
in the output grid, preserving the block's color and length, keeping the 
background white, and maintaining the 1xN grid structure.
"""

def find_non_white_block(grid_row):
    """
    Finds the start column index, end column index (exclusive), and color 
    of the first contiguous block of non-white pixels in a 1D array 
    representing a grid row.

    Args:
        grid_row (np.array): A 1D numpy array representing a row of the grid.

    Returns:
        tuple: (start_index, end_index, color) or (None, None, None) if no block found.
    """
    start_index = -1
    end_index = -1
    color = -1
    
    # Iterate through the pixels of the row
    for i, pixel in enumerate(grid_row):
        if pixel != 0:  # Found a non-white pixel
            if start_index == -1: # Start of a potential block
                start_index = i
                color = pixel
            # Ensure the block is contiguous and of the same color
            elif pixel != color: 
                # Found a different color, marks the end of the first block
                end_index = i 
                break 
        elif start_index != -1: # Found a white pixel after the block started
            # This marks the end of the block
            end_index = i
            break
            
    # If the block extends to the very end of the row
    if start_index != -1 and end_index == -1:
        end_index = len(grid_row)
        
    # Return findings or None if no block was found
    if start_index != -1:
        return start_index, end_index, color
    else:
        return None, None, None


def transform(input_grid):
    """
    Transforms the input grid by shifting the single non-white block 
    within its row 3 positions to the right.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid, 
                                       expected to have exactly one row.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Validate input structure (should be 1xN)
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        # Handle unexpected input format if necessary, though ARC standard guarantees grids
        # For this specific task based on examples, we strictly expect one row.
        # Returning the input as is or raising an error might be options depending on requirements.
        # Given the context, let's assume valid input matching examples.
        pass 

    # Extract the single row as a numpy array for easier manipulation
    input_row = np.array(input_grid[0], dtype=int)
    grid_width = len(input_row)
    
    # Initialize the output row with the same width and background color (white=0)
    output_row = np.zeros(grid_width, dtype=int)
    
    # Find the non-white block in the input row
    start_index, end_index, color = find_non_white_block(input_row)
    
    # If a block was found, perform the shift
    if start_index is not None:
        # Calculate the new desired start and end positions
        new_start_index = start_index + 3
        new_end_index = end_index + 3
        
        # Determine the actual start and end indices within the output grid bounds
        # This clips the block if the shift pushes it partially or fully off the grid edge
        actual_start = max(0, new_start_index)
        actual_end = min(grid_width, new_end_index)
        
        # Determine the length of the block segment to actually place in the output
        # If actual_start >= actual_end, the block is shifted entirely off the grid
        actual_length = actual_end - actual_start

        # Place the block (or the visible part of it) into the output row
        if actual_length > 0:
            # Calculate the corresponding start index in the original block
            # This is needed if the block starts off the left edge after clipping
            original_block_start_offset = actual_start - new_start_index
             
            # Fill the corresponding section of the output row with the block's color
            output_row[actual_start:actual_end] = color

    # Return the modified output row wrapped in a list to match the 2D grid format
    return [output_row.tolist()]