import numpy as np

"""
Shift a contiguous block of non-white pixels 3 positions to the right within a 1D grid.
The input grid is assumed to be 1xN.
The background color is white (0).
The transformation identifies the single contiguous block of non-white pixels,
creates a new grid filled with the background color, and copies the block
into the new grid, shifted 3 positions to the right from its original starting position.
"""

def find_contiguous_non_white_block(row):
    """
    Finds the start and end indices of the first contiguous block of non-white pixels.

    Args:
        row (np.array): A 1D numpy array representing a row of the grid.

    Returns:
        tuple: (start_index, end_index) of the block, or (None, None) if no block found.
    """
    non_white_indices = np.where(row != 0)[0]
    if len(non_white_indices) == 0:
        return None, None  # No non-white pixels found

    start_index = non_white_indices[0]
    # Check for contiguity - assumes only *one* block exists based on examples
    # Find the last index in the sequence that is contiguous
    end_index = start_index
    for i in range(1, len(non_white_indices)):
        if non_white_indices[i] == non_white_indices[i-1] + 1:
            end_index = non_white_indices[i]
        else:
            # This handles cases with multiple blocks, but based on examples,
            # we assume only one block, so we break after the first contiguous one.
            break
            
    # Alternative simpler assumption if *all* non-white pixels form one block:
    # end_index = non_white_indices[-1]

    return start_index, end_index

def transform(input_grid):
    """
    Shifts a contiguous block of non-white pixels 3 positions to the right.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid (assumed 1xN).

    Returns:
        np.array: The transformed grid with the block shifted.
    """
    # Ensure input is a numpy array
    input_grid = np.array(input_grid)
    
    # Assume the grid is 1xN, work with the first row
    input_row = input_grid[0]
    grid_height, grid_width = input_grid.shape

    # Initialize output_grid with the same shape and background color (0)
    output_grid = np.zeros_like(input_grid)
    output_row = output_grid[0] # Get a reference to the row to modify

    # Find the contiguous block of non-white pixels in the input row
    start_index, end_index = find_contiguous_non_white_block(input_row)

    # If a block is found, shift it
    if start_index is not None:
        # Extract the block pixels
        block_pixels = input_row[start_index : end_index + 1]
        block_length = len(block_pixels)

        # Calculate the new starting position
        new_start_index = start_index + 3
        new_end_index = new_start_index + block_length # Exclusive index for slicing

        # Check if the new position is within the grid bounds
        if new_start_index < grid_width:
            # Ensure the block doesn't go past the right edge
            place_end_index = min(new_end_index, grid_width)
            place_length = place_end_index - new_start_index
            
            # Place the block (or the part that fits) in the output row
            output_row[new_start_index : place_end_index] = block_pixels[:place_length]

    # Return the modified grid
    return output_grid