import numpy as np
from typing import Tuple, Optional

"""
Transforms a 1xN input grid by identifying a single contiguous block of 
non-white pixels in the row, shifting this block two positions to the right, 
and placing it in an otherwise white output grid of the same dimensions.
"""

def find_non_white_block_in_row(row: np.ndarray) -> Optional[Tuple[int, int, int]]:
    """
    Finds the first contiguous block of non-white pixels in a 1D array.

    Args:
        row: The input 1D numpy array representing the row.

    Returns:
        A tuple (color, start_index, length) if a block is found,
        otherwise None.
    """
    start_index = -1
    color = -1
    length = 0
    block_found = False

    for i, pixel in enumerate(row):
        if pixel != 0:  # Found a non-white pixel
            if not block_found:  # Start of the block
                start_index = i
                color = pixel
                length = 1
                block_found = True
            elif pixel == color: # Continuation of the current block
                 length += 1
            else: # Found a different non-white color - stop (assume only one block)
                 break
        elif block_found: # Found white after a block started
            # Block ended
            break # Assuming only one block needs to be found

    if block_found:
        return int(color), start_index, length
    else:
        return None

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by shifting the non-white block right by 2 positions.

    Args:
        input_grid: A numpy array of shape (1, N) representing the input grid.

    Returns:
        A numpy array of the same shape representing the transformed output grid.
    """
    # Ensure input is a 2D numpy array with one row
    if not isinstance(input_grid, np.ndarray) or input_grid.ndim != 2 or input_grid.shape[0] != 1:
         raise ValueError("Input must be a 2D NumPy array with exactly one row.")

    # Extract the first (and only) row
    input_row = input_grid[0]
    grid_height, grid_width = input_grid.shape

    # Initialize the output grid with white pixels (0)
    output_grid = np.zeros_like(input_grid)

    # Find the non-white block in the input row
    block_info = find_non_white_block_in_row(input_row)

    if block_info:
        color, start_index, length = block_info

        # Calculate the new starting position (shifted right by 2)
        new_start_index = start_index + 2

        # Place the block in the output grid's first row at the new position
        # Ensure the block doesn't go out of bounds
        for i in range(length):
            target_index = new_start_index + i
            # Check if the target index is within the grid width
            if target_index < grid_width:
                output_grid[0, target_index] = color
            else:
                # Stop if the block goes past the end of the grid width
                break

    return output_grid