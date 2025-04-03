import numpy as np
from typing import Tuple, Optional

"""
Identifies the single contiguous block of non-white (non-zero) pixels 
within the input grid's single row. Shifts this block one position to 
the right, if possible. The shift involves changing the leftmost pixel 
of the original block to white (0) and changing the white pixel 
immediately to the right of the block's original position to the block's 
color. If the block is already at the rightmost edge, no change occurs. 
The output grid retains the same dimensions as the input grid.
"""

def find_contiguous_block(row: np.ndarray, background_color: int = 0) -> Optional[Tuple[int, int, int]]:
    """
    Finds the first contiguous block of non-background color in a 1D numpy array.

    Args:
        row: The 1D numpy array (row) of pixel values.
        background_color: The value representing the background color.

    Returns:
        A tuple containing (block_color, start_index, end_index) if a block is found,
        otherwise returns None.
    """
    start_index = -1
    end_index = -1
    block_color = -1

    for i, pixel in enumerate(row):
        # Start of a potential block
        if pixel != background_color and start_index == -1:
            start_index = i
            block_color = pixel
            end_index = i # Initialize end_index
        # Continuation of the block
        elif pixel == block_color and start_index != -1:
            end_index = i
        # End of the block (found background or different color after block started)
        elif pixel != block_color and start_index != -1:
            break # Found the end of the block

    if start_index != -1:
        return block_color, start_index, end_index
    else:
        return None


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Shifts the contiguous non-white block in the single row of the input grid
    one position to the right, if possible.

    Args:
        input_grid: A 2D numpy array representing the input grid (expected 1xN).

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    # Ensure input is a numpy array and has at least one row
    if not isinstance(input_grid, np.ndarray) or input_grid.shape[0] < 1:
        raise ValueError("Input must be a NumPy array with at least one row.")
        
    # Extract the first row (assuming input is always 1xN as per examples)
    row = input_grid[0]
    row_length = len(row)
    background_color = 0

    # Find the contiguous block in the row
    block_info = find_contiguous_block(row, background_color)

    # Initialize output_grid as a copy of the input grid
    # We create a copy early to handle cases where no block is found or shift is not possible
    output_grid = np.copy(input_grid)

    # Proceed only if a block was found
    if block_info:
        block_color, start_index, end_index = block_info

        # Check if the shift is possible (block not at the rightmost edge)
        if (end_index + 1) < row_length:
            # Perform the shift on the first row of the output grid
            # Change the original start position to background
            output_grid[0, start_index] = background_color
            # Change the position after the original end position to the block color
            output_grid[0, end_index + 1] = block_color
        # If shift is not possible (block at the edge), the copied grid remains unchanged.

    # If no block was found, the original copied grid is returned.
    return output_grid