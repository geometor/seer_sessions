import numpy as np
import copy

"""
Identify the longest contiguous horizontal block of orange (7) pixels within the input grid (which is effectively a single row). 
If there are multiple blocks of the same maximum length, select the rightmost one (the one with the highest starting index).
Replace the pixels of this selected block with gray (5) pixels in the output grid. 
All other pixels remain unchanged.
"""

def find_longest_orange_block(grid_row):
    """
    Finds the start index and length of the longest contiguous block of orange (7) pixels.
    Handles ties by selecting the rightmost block.

    Args:
        grid_row (list or np.array): The single row of the grid.

    Returns:
        tuple: (start_index, length) of the longest orange block, or (-1, 0) if no orange block exists.
    """
    max_length = 0
    best_start = -1
    current_start = -1
    current_length = 0

    for i, pixel in enumerate(grid_row):
        if pixel == 7:
            # Start of a new block or continuation of the current one
            if current_length == 0:
                current_start = i
            current_length += 1
        else:
            # End of a potential block
            if current_length > 0:
                # Check if this block is the longest so far, or equal length but further right
                if current_length >= max_length:
                    max_length = current_length
                    best_start = current_start
                # Reset current block tracking
                current_start = -1
                current_length = 0

    # Check if the grid ended with an orange block
    if current_length > 0:
        if current_length >= max_length:
            max_length = current_length
            best_start = current_start
            
    return best_start, max_length

def transform(input_grid):
    """
    Transforms the input grid by finding the longest contiguous block of orange (7) pixels 
    (rightmost in case of ties) and replacing it with gray (5) pixels.

    Args:
        input_grid (list of lists or np.array): The input grid. 
                                                 Assumed to be effectively 1D for this task.

    Returns:
        list of lists or np.array: The transformed grid.
    """
    # Ensure input is a numpy array for easier handling, especially if it's multi-row
    input_array = np.array(input_grid, dtype=int)
    
    # Make a copy to modify
    output_grid = np.copy(input_array)

    # Since the examples are effectively 1D, we operate on the first row
    # If the input could be truly 2D but the logic applies row-wise, 
    # we would need to loop through rows. Based on examples, assume 1 row.
    if input_array.shape[0] == 1:
        grid_row = input_array[0]

        # Find the longest orange block (rightmost tiebreak)
        start_index, length = find_longest_orange_block(grid_row)

        # If a valid block was found, modify the output grid
        if start_index != -1 and length > 0:
            for i in range(start_index, start_index + length):
                # Check bounds just in case, though logic should prevent out-of-bounds
                if i < output_grid.shape[1]: 
                    output_grid[0, i] = 5 # Change to gray
    
    # Convert back to list of lists if that's the desired format
    return output_grid.tolist()
