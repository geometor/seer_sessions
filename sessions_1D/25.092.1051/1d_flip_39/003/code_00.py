import numpy as np

"""
Identifies a contiguous block of non-white pixels within the single row of a 1xN input grid. 
Moves the first pixel of this block (which is always magenta, color 6) to the end of the block. 
The other pixels within the block are shifted one position to the left to fill the gap. 
Pixels outside this block (the surrounding white pixels) remain unchanged.
"""

def find_non_white_block(grid_row):
    """
    Finds the start and end indices (inclusive) of the first contiguous block 
    of non-white (non-zero) pixels in a 1D NumPy array.

    Args:
        grid_row: A 1D NumPy array representing the grid row.

    Returns:
        A tuple (start_index, end_index) if a block is found, otherwise None.
    """
    start_index = -1
    end_index = -1
    in_block = False
    for i, pixel in enumerate(grid_row):
        if pixel != 0 and not in_block:
            start_index = i
            in_block = True
        if pixel != 0 and in_block:
            end_index = i # Keep updating end_index while in block
        elif pixel == 0 and in_block:
            # Found the end of the block
            break 
            
    if start_index != -1:
        return start_index, end_index
    else:
        # No non-white pixels found at all
        return None

def transform(input_grid):
    """
    Transforms the input grid by finding a non-white block in the single row
    and moving its first element (magenta, 6) to the end of the block.

    Args:
        input_grid: A 1xN NumPy array representing the input grid.

    Returns:
        A 1xN NumPy array representing the transformed output grid.
    """
    # Ensure input is a NumPy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)

    # Initialize output_grid as a copy of the input to avoid modifying the original
    output_grid = np.copy(input_grid)

    # Check if the grid has at least one row
    if input_grid.shape[0] == 0:
        return output_grid # Return empty grid if input is empty

    # Extract the single row (assuming input is always 1xN)
    # If input could potentially have more rows, add error handling or logic
    if input_grid.shape[0] != 1:
         # For this specific problem, we assume 1 row based on examples.
         # If the requirement changes, this needs adjustment.
         # For now, let's proceed assuming the first row is the target.
         pass # Or raise an error: raise ValueError("Input grid must have exactly one row")
         
    row = input_grid[0]
    output_row = output_grid[0] # Get a view to modify the output grid directly

    # Find the contiguous block of non-white pixels in the row
    block_indices = find_non_white_block(row)

    # If a block is found, perform the transformation
    if block_indices:
        start_index, end_index = block_indices
        
        # Extract the block from the original row
        block = row[start_index : end_index + 1]

        # Check if the block is non-empty and starts with the expected color (magenta 6)
        if block.size > 0 and block[0] == 6:
            # Extract the first pixel (magenta)
            first_pixel = block[0]
            # Extract the rest of the pixels in the block
            other_pixels = block[1:]
            
            # Construct the new block: other pixels followed by the first pixel
            # Ensure first_pixel is treated as an array element for concatenation
            new_block = np.concatenate((other_pixels, np.array([first_pixel]))) 
            
            # Replace the original block segment in the output row with the new block
            output_row[start_index : end_index + 1] = new_block
            
    # Return the modified output grid
    return output_grid