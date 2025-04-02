import numpy as np

"""
Identifies a single contiguous horizontal block of non-white pixels in the 
input grid (which is always 1xN). Creates an output grid of the same size, 
initially filled with white (0). Shifts the identified block 2 positions to 
the right in the output grid, preserving its color and length.
"""

def find_horizontal_block(row):
    """
    Finds the start index, end index, and color of the first contiguous 
    horizontal block of non-white pixels in a 1D array (row).
    
    Args:
        row (np.array): A 1D numpy array representing a row of the grid.
        
    Returns:
        tuple: (start_index, end_index, color) or (None, None, None) if no 
               non-white block is found.
    """
    non_white_indices = np.where(row != 0)[0]
    if len(non_white_indices) == 0:
        return None, None, None

    start_index = non_white_indices[0]
    end_index = non_white_indices[-1]
    
    # Verify contiguity (optional but good practice for general cases)
    # For this specific task, examples suggest it's always one block.
    # if not np.all(np.diff(non_white_indices) == 1):
        # Handle cases with multiple blocks or gaps if necessary
        # Based on examples, assume one contiguous block.
        
    color = row[start_index]  # Get color from the first pixel of the block
    
    return start_index, end_index, color

def transform(input_grid):
    """
    Shifts the single horizontal non-white block in a 1xN grid 2 positions 
    to the right.

    Args:
        input_grid (list of lists): A 1xN grid containing integers 0-9.

    Returns:
        list of lists: The transformed 1xN grid.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # Initialize output grid with background color (white, 0)
    output_array = np.zeros_like(input_array)

    # The grid is always 1 row high, so operate on the first row
    if height > 0:
        input_row = input_array[0]
        
        # 1. Identify the single contiguous horizontal block
        start_index, end_index, block_color = find_horizontal_block(input_row)

        # Proceed only if a block was found
        if start_index is not None:
            # 2. Calculate the new starting and ending column indices (shift right by 2)
            new_start = start_index + 2
            new_end = end_index + 2

            # 3. Fill the cells in the output grid at the new position
            # Ensure the new indices are within the grid boundaries
            # Calculate the range of indices to fill in the output row
            fill_start = max(0, new_start)
            fill_end = min(width, new_end + 1) # Slice goes up to, but not including, the end index

            if fill_start < fill_end: # Check if there's anything to fill
                 output_array[0, fill_start:fill_end] = block_color

    # Convert the result back to a list of lists
    return output_array.tolist()