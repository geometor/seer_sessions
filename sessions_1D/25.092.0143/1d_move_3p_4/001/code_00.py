import numpy as np

"""
Identifies a single contiguous block of non-white pixels in the input row, 
then shifts this block 3 positions to the right in the output row, 
maintaining the block's color and length, and keeping the background white.
"""

def find_colored_block(row):
    """
    Finds the first contiguous block of non-white pixels in a 1D array.

    Args:
        row (np.array): A 1D numpy array representing a row of the grid.

    Returns:
        tuple: (color, start_index, length) of the block, or None if no block is found.
    """
    start_index = -1
    color = 0
    length = 0
    width = len(row)
    
    for i in range(width):
        if row[i] != 0:  # Found the start of a block
            color = row[i]
            start_index = i
            length = 1
            # Find the end of the block
            for j in range(i + 1, width):
                if row[j] == color:
                    length += 1
                else:
                    break  # End of the block
            return color, start_index, length
            
    return None # No non-white block found

def transform(input_grid):
    """
    Shifts the single colored block found in the input row 3 positions to the right.

    Args:
        input_grid (list of lists): A grid represented as a list of lists. 
                                     Expected to have only one row.

    Returns:
        list of lists: The transformed grid with the colored block shifted.
    """
    # Convert input to numpy array for easier manipulation
    np_input = np.array(input_grid, dtype=int)
    
    # Assuming the grid is always 1 row high based on examples
    if np_input.shape[0] != 1:
        # Handle unexpected input dimensions if necessary, 
        # for now, just process the first row or raise error
        # Based on examples, we expect shape (1, width)
        # If this assumption is wrong, the logic might need adjustment.
        pass # Or raise ValueError("Input grid must have exactly one row")

    input_row = np_input[0]
    height, width = np_input.shape
    
    # Initialize output grid with the same dimensions, filled with white (0)
    output_grid = np.zeros_like(np_input)
    
    # Find the colored block in the input row
    block_info = find_colored_block(input_row)
    
    if block_info:
        color, start_index, length = block_info
        
        # Calculate the new starting position
        new_start_index = start_index + 3
        
        # Calculate the new ending position (exclusive)
        new_end_index = new_start_index + length
        
        # Check boundaries: Ensure the block fits within the grid width
        if new_start_index < width:
             # Make sure we don't write past the end of the array
            write_length = min(length, width - new_start_index)
            actual_end_index = new_start_index + write_length
           
            # Place the block in the output grid at the new position
            output_grid[0, new_start_index:actual_end_index] = color
    # else: if no block found, output_grid remains all white (zeros), which is correct.

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()