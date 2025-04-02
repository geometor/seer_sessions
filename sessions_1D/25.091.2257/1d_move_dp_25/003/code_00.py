"""
Move the contiguous block of white pixels (0) preceding the single orange pixel (7) in a 1xN grid to the beginning of the grid row.
"""

import numpy as np

# Constants for pixel values
ORANGE = 7
WHITE = 0

def find_orange_pixel_index(grid_1d: np.ndarray) -> int:
    """Finds the index of the first occurrence of the orange pixel in a 1D array."""
    indices = np.where(grid_1d == ORANGE)[0]
    if len(indices) > 0:
        return indices[0]
    else:
        # Handle case where orange pixel is not found.
        # Based on examples, it should always be present.
        return -1 

def find_preceding_white_segment_indices(grid_1d: np.ndarray, orange_index: int) -> tuple[int, int]:
    """
    Finds the start and end indices (exclusive end) of the contiguous white segment 
    immediately before the orange pixel in a 1D array.
    Returns (start_index, end_index).
    If no white segment exists, start_index will equal end_index (which is orange_index).
    """
    if orange_index == 0:
        # Orange pixel is at the beginning, no preceding segment possible.
        return 0, 0

    # The segment ends just before the orange pixel
    end_index = orange_index 
    start_index = orange_index

    # Iterate backwards from the position just before the orange pixel
    for i in range(orange_index - 1, -1, -1):
        if grid_1d[i] == WHITE:
            start_index = i  # Update start index if white pixel found
        else:
            # Stop when a non-white pixel is encountered
            break
            
    return start_index, end_index

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the 1xN input grid by finding the contiguous block of white pixels (0) 
    immediately preceding the single orange pixel (7) and moving this block to 
    the beginning of the grid row.

    Args:
        input_grid: A 1xN numpy array representing the input grid.

    Returns:
        A 1xN numpy array representing the transformed output grid.
    """
    # Ensure the input is a 2D array with one row
    if input_grid.ndim != 2 or input_grid.shape[0] != 1:
        # Handle unexpected input dimensions if necessary, or raise an error
        # For now, assume valid input based on examples
        print("Warning: Input grid shape is not 1xN. Proceeding with the first row.")
        if input_grid.ndim == 1:
             grid_1d = input_grid # Treat 1D array as the row
        else:
             grid_1d = input_grid[0] # Use the first row     
    else:
        # Extract the single row as a 1D array for easier processing
        grid_1d = input_grid[0]

    # Find the index of the orange pixel (7).
    orange_idx = find_orange_pixel_index(grid_1d)
    
    # If orange pixel isn't found, return the original grid unchanged
    if orange_idx == -1:
        return input_grid.copy() 

    # Identify the contiguous sequence of white pixels (0) immediately preceding the orange pixel.
    # white_segment_end is effectively orange_idx
    white_segment_start, white_segment_end = find_preceding_white_segment_indices(grid_1d, orange_idx)
    
    # Extract the segments using numpy slicing
    # The white segment to be moved
    white_segment = grid_1d[white_segment_start:white_segment_end]
    
    # The part of the grid before the white segment
    prefix = grid_1d[:white_segment_start]
    
    # The part of the grid from the orange pixel onwards (which is the same as from white_segment_end onwards)
    suffix = grid_1d[white_segment_end:] 

    # Construct the new 1D array by concatenating segments in the desired order
    # Order: white_segment + prefix + suffix
    output_grid_1d = np.concatenate((white_segment, prefix, suffix))
    
    # Reshape the 1D array back to the original 1xN shape
    # -1 automatically calculates the correct number of columns
    output_grid = output_grid_1d.reshape(1, -1) 

    return output_grid