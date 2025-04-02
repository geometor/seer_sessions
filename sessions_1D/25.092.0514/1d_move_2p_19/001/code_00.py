import numpy as np

"""
The transformation identifies a single contiguous block of non-white pixels in a 
single-row input grid and shifts this block 2 positions to the right in the 
output grid. The output grid has the same dimensions as the input, and areas 
not occupied by the shifted block are filled with white pixels (0).
"""

def transform(input_grid):
    """
    Shifts the single contiguous non-white block in a 1D grid 2 positions right.

    Args:
        input_grid (list of lists): A grid representing the input state, 
                                    expected to have only one row.

    Returns:
        list of lists: A new grid with the block shifted 2 positions right.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    
    # Get grid dimensions (height should be 1)
    height, width = grid.shape
    
    # Initialize output grid with the same dimensions, filled with white (0)
    output_grid = np.zeros_like(grid)
    
    # Extract the single row (assuming height is always 1 based on examples)
    if height != 1:
        # Handle unexpected input format if necessary, though examples are 1xN
        # For now, let's proceed assuming height is 1
        pass 
        
    row = grid[0]

    # Find the indices of non-white pixels
    non_white_indices = np.where(row != 0)[0]

    # If no non-white pixels are found, return the empty output grid
    if len(non_white_indices) == 0:
        return output_grid.tolist()

    # Identify the start and end of the contiguous block
    # Assumes only one contiguous block exists, as per perception
    start_index = non_white_indices[0]
    end_index = non_white_indices[-1] # Inclusive index of the last block pixel

    # Extract the block's pixel values
    block = row[start_index : end_index + 1]
    block_length = len(block)

    # Calculate the new starting position for the block
    new_start_index = start_index + 2

    # Determine the segment of the block that fits within the grid boundaries
    # Calculate how many pixels of the block can actually be placed
    placeable_length = max(0, min(block_length, width - new_start_index))
    
    # Place the block (or the portion that fits) into the output grid
    if placeable_length > 0:
        # Calculate the actual end position in the output grid (exclusive)
        new_end_pos_exclusive = new_start_index + placeable_length
        # Slice the block if only a portion fits
        block_to_place = block[:placeable_length]
        # Assign the block pixels to the calculated position in the output grid's first row
        output_grid[0, new_start_index:new_end_pos_exclusive] = block_to_place

    # Convert the result back to a list of lists before returning
    return output_grid.tolist()