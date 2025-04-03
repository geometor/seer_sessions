import numpy as np

"""
Identifies a contiguous horizontal block of non-white pixels in a 1D input grid 
and shifts this block one position to the right in the output grid. The original 
location of the leftmost pixel of the block becomes white, and the pixel to the 
right of the block's original rightmost position takes the block's color.
"""

def find_non_white_block(grid):
    """
    Finds the start index, end index, and color of the first contiguous 
    non-white block in a 1D grid.

    Args:
        grid (np.array): A 1D numpy array representing the input grid row.

    Returns:
        tuple: (start_index, end_index, color) or (None, None, None) if no 
               non-white block is found.
    """
    non_white_indices = np.where(grid != 0)[0]
    if len(non_white_indices) == 0:
        return None, None, None  # No non-white pixels

    start_index = non_white_indices[0]
    color = grid[start_index]
    
    # Find the end of the contiguous block of the *same* color
    end_index = start_index
    for i in range(start_index + 1, len(grid)):
        if grid[i] == color:
            end_index = i
        else:
            break # Stop when the color changes or we hit a white pixel

    return start_index, end_index, color

def transform(input_grid):
    """
    Shifts a contiguous non-white block one position to the right.

    Args:
        input_grid (np.array): A 1D numpy array representing the input grid row.

    Returns:
        np.array: A 1D numpy array representing the transformed output grid row.
    """
    # Ensure input is a 1D array (or handle 2D case if needed, assuming single row for now)
    if input_grid.ndim > 1:
        if input_grid.shape[0] == 1:
             grid_row = input_grid[0] # Work with the first row if it's 2D but has only 1 row
        else:
             # Handle multi-row case or raise error if unexpected
             raise ValueError("Input grid must be 1D or have only one row for this transformation")
    else:
        grid_row = input_grid

    height = 1
    width = len(grid_row)

    # Initialize output grid with the background color (white)
    output_grid_row = np.zeros_like(grid_row)

    # Find the non-white block in the input row
    start_idx, end_idx, block_color = find_non_white_block(grid_row)

    # If a block is found, shift it
    if start_idx is not None:
        # Calculate the new position
        new_start_idx = start_idx + 1
        new_end_idx = end_idx + 1

        # Calculate the length of the block
        block_length = end_idx - start_idx + 1

        # Check if the shifted block fits within the grid boundaries
        if new_end_idx < width:
            # Place the shifted block in the output grid
            output_grid_row[new_start_idx : new_end_idx + 1] = block_color
        # else: the block shifts off the grid, resulting in an all-white output (already initialized)
        
    # Reshape back to 2D if the input was 2D (1xN)
    if input_grid.ndim > 1:
        return output_grid_row.reshape(1, width)
    else:
        return output_grid_row
