"""
Shift a contiguous block of a non-white, non-blue color rightwards within its 
row until it is adjacent to (immediately to the left of) a stationary blue 
marker pixel in the same row. The input and output are 2D grids containing 
only one row.
"""

import numpy as np
from typing import Tuple, Optional

# Helper function to find the contiguous colored block (non-white, non-blue)
def find_colored_block(grid_row: np.ndarray) -> Optional[Tuple[int, int, int]]:
    """
    Finds the first contiguous block of non-white (0) and non-blue (1) pixels
    within a given row.

    Args:
        grid_row: A 1D NumPy array representing the grid row.

    Returns:
        A tuple containing (color, start_index, end_index) of the block,
        or None if no such block is found.
    """
    start_index = -1
    color = -1
    for i, pixel_val in enumerate(grid_row):
        # Ensure we are comparing integers
        pixel_val = int(pixel_val) 
        
        if pixel_val != 0 and pixel_val != 1: # Found a pixel of the target block color
            if start_index == -1: # Starting a new block
                start_index = i
                color = pixel_val
            elif pixel_val != color: # Color changed, meaning end of the first block
                 # This assumes only ONE block, consistent with examples.
                 return (color, start_index, i - 1)
        elif start_index != -1: # Block was ongoing, but now hit a 0 or 1
            # Block ended
            return (color, start_index, i - 1)
            
    # Handle case where the block extends to the end of the grid row
    if start_index != -1:
        return (color, start_index, len(grid_row) - 1)
        
    return None # No block found

# Helper function to find the blue marker
def find_blue_marker(grid_row: np.ndarray) -> Optional[int]:
    """
    Finds the index (column) of the blue (1) marker pixel within a given row.

    Args:
        grid_row: A 1D NumPy array representing the grid row.

    Returns:
        The index of the blue marker, or None if not found.
    """
    for i, pixel_val in enumerate(grid_row):
        if int(pixel_val) == 1: # Found the blue marker
            return i
    return None # No blue marker found

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Shifts a colored block rightwards in the single row of the grid 
    to abut a stationary blue marker.

    Args:
        input_grid: A 2D NumPy array representing the input grid (expected 1 row).

    Returns:
        A 2D NumPy array representing the transformed grid.
    """
    # Ensure input is a numpy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)
        
    # Verify input is 2D and extract the first row
    if input_grid.ndim != 2 or input_grid.shape[0] != 1:
        # Handle unexpected input dimensions if necessary, 
        # but based on examples, assume 1 row.
        # For robustness, maybe raise an error or return input as is.
        # Here, we proceed assuming the first row is the target.
        pass # Or add error handling
        
    input_row = input_grid[0]
    grid_width = input_row.shape[0]

    # Find the colored block in the row
    block_info = find_colored_block(input_row)
    if block_info is None:
        # Should not happen based on task description/examples
        return input_grid.copy() # Return original if no block found

    block_color, block_start, block_end = block_info
    block_length = block_end - block_start + 1

    # Find the blue marker in the row
    marker_index = find_blue_marker(input_row)
    if marker_index is None:
        # Should not happen based on task description/examples
        return input_grid.copy() # Return original if no marker found
        
    # Calculate the target end position for the block (right before the marker)
    new_block_end = marker_index - 1
    
    # Calculate the required shift amount
    shift_amount = new_block_end - block_end
    
    # Calculate the new start position for the block
    new_block_start = block_start + shift_amount

    # Initialize the output row with white (0) pixels
    output_row = np.zeros(grid_width, dtype=int)

    # Place the shifted colored block into the output row
    # Ensure indices are within bounds
    if new_block_start >= 0 and new_block_start + block_length <= grid_width:
        output_row[new_block_start : new_block_start + block_length] = block_color

    # Place the blue marker at its original position in the output row
    if 0 <= marker_index < grid_width:
        output_row[marker_index] = 1
        
    # Reshape the 1D output row back into a 2D grid with 1 row
    output_grid = output_row.reshape(1, grid_width)

    return output_grid