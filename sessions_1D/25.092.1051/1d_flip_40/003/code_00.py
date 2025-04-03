import numpy as np
import copy

"""
Identifies the single contiguous sequence of non-white (non-zero) pixels in a 1D input grid. 
Performs a left cyclic shift on this sequence: the first pixel of the sequence moves 
to the end of the sequence, and all other pixels in the sequence shift one position 
to the left. White (zero) pixels outside this sequence remain unchanged. If no 
non-white sequence exists, or the sequence has only one pixel, the grid is returned unmodified.
"""

def find_contiguous_non_white_block(grid_1d):
    """
    Finds the start and end indices of the first contiguous block of non-zero values.

    Args:
        grid_1d (np.array): A 1D numpy array representing the grid row.

    Returns:
        tuple: A tuple containing (start_index, end_index) if a block is found,
               otherwise returns (None, None).
    """
    # Find indices of all non-white pixels
    non_white_indices = np.where(grid_1d != 0)[0]
    
    # Handle case with no non-white pixels
    if len(non_white_indices) == 0:
        return None, None 

    # The start index is the first non-white index
    start_index = non_white_indices[0]
    end_index = start_index

    # Iterate through the rest of the non-white indices to find the end of the *first* contiguous block
    for i in range(1, len(non_white_indices)):
        # If the current index is adjacent to the previous one, extend the block
        if non_white_indices[i] == end_index + 1:
            end_index = non_white_indices[i]
        else:
            # Found a gap, so the first contiguous block has ended
            break 
            
    return start_index, end_index


def transform(input_grid):
    """
    Applies a left cyclic shift to the contiguous non-white block in a 1D grid.

    Args:
        input_grid (list or np.array): A 1D list or numpy array representing the input grid row.

    Returns:
        np.array: A 1D numpy array representing the transformed grid row.
    """
    # Convert input to numpy array for easier manipulation
    grid_1d = np.array(input_grid)
    
    # Initialize output_grid as a copy of the input
    output_grid = grid_1d.copy()

    # 1. Identify the contiguous sequence of non-white pixels
    start_index, end_index = find_contiguous_non_white_block(grid_1d)

    # 2. If no non-white sequence exists, or it's just one pixel, return the original grid copy
    #    (np.roll on a single element array returns the array unchanged, so we could technically
    #     omit the 'start_index == end_index' check, but explicitly handling it is clear).
    if start_index is None or start_index == end_index:
        return output_grid
        
    # 3. If a non-white sequence exists and has more than one element:
    #   a. Extract the sequence (block)
    block = grid_1d[start_index : end_index + 1]

    #   b. Perform left cyclic shift on the extracted block
    #      np.roll(array, shift) shifts elements. Negative shift is left.
    shifted_block = np.roll(block, -1)

    #   c. Place the shifted sequence back into the output grid
    output_grid[start_index : end_index + 1] = shifted_block

    # 4. Return the modified output grid
    return output_grid