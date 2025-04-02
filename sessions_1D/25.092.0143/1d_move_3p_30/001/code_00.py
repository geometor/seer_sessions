import numpy as np

"""
Identifies a single contiguous block of non-white pixels in a 1D input grid (represented as a 1xN array).
Shifts this block exactly 3 positions to the right.
The output grid has the same dimensions as the input, with the background remaining white (0) and the shifted block retaining its original color and length.
"""

def find_colored_block(grid_row):
    """
    Finds the start index, length, and color of the first contiguous non-zero block in a 1D array.

    Args:
        grid_row (np.array): A 1D numpy array representing a row of the grid.

    Returns:
        tuple: (start_index, length, color) or (None, 0, 0) if no block is found.
    """
    start_index = -1
    length = 0
    color = 0
    width = len(grid_row)

    for i in range(width):
        pixel = grid_row[i]
        if pixel != 0:  # Found the start of a block or continuation
            if start_index == -1: # Start of a new block
                start_index = i
                color = pixel
                length = 1
            elif pixel == color: # Continuation of the current block
                 length += 1
            else: # Different color, implies end of the first block (shouldn't happen based on examples)
                break
        elif start_index != -1: # Found a 0 after the block started, block ended
            break
            
    if start_index == -1: # No block found
        return None, 0, 0
        
    return start_index, length, color

def transform(input_grid):
    """
    Transforms the input grid by shifting the colored block 3 positions to the right.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Get grid dimensions (assuming 1 row based on examples)
    height, width = input_np.shape
    
    # Initialize output grid with the same dimensions, filled with background color (0)
    output_np = np.zeros_like(input_np)
    
    # Since the grid is 1D (1 row), operate on the first row
    if height == 1:
        grid_row = input_np[0]
        
        # Find the colored block in the input row
        start_index, length, color = find_colored_block(grid_row)
        
        # If a block was found, calculate its new position and place it in the output
        if start_index is not None:
            # Calculate the new starting position
            new_start_index = start_index + 3
            
            # Calculate the end index (exclusive)
            new_end_index = new_start_index + length
            
            # Ensure the new block fits within the grid boundaries
            if new_start_index >= 0 and new_end_index <= width:
                 # Place the block in the output grid
                 output_np[0, new_start_index:new_end_index] = color
            # else: handle cases where the block shifts off-grid (not seen in examples, default is it disappears)

    # Convert the numpy array back to a list of lists for the standard ARC format
    output_grid = output_np.tolist()
    
    return output_grid