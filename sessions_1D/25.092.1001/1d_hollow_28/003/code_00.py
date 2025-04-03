"""
Identifies a single horizontal contiguous block of non-white pixels within a single-row 2D NumPy array. 
Preserves the first (start_index) and last (end_index) pixel of this block. 
Changes all pixels strictly between the start_index and end_index of the block to white (0). 
Pixels outside the block (including original white pixels) remain unchanged.
The function returns the modified 2D NumPy array.
"""

import numpy as np

def find_non_white_block_indices(row):
    """
    Finds the indices of non-white pixels in a 1D array.

    Args:
        row (np.array): A 1D numpy array representing a row of the grid.

    Returns:
        tuple: A tuple containing (non_white_indices, start_index, end_index).
               non_white_indices is an array of indices.
               start_index is the minimum index, or None if no non-white pixels.
               end_index is the maximum index, or None if no non-white pixels.
    """
    non_white_indices = np.where(row != 0)[0]
    if len(non_white_indices) == 0:
        return non_white_indices, None, None
    
    start_index = np.min(non_white_indices)
    end_index = np.max(non_white_indices)
    return non_white_indices, start_index, end_index

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.array): A 2D NumPy array, expected shape (1, width).

    Returns:
        np.array: The transformed 2D NumPy array.
    """
    # Ensure input is a NumPy array
    if not isinstance(input_grid, np.ndarray):
        raise TypeError("Input grid must be a NumPy array.")

    # Validate shape (optional but good practice based on examples)
    if input_grid.ndim != 2 or input_grid.shape[0] != 1:
         # Handle unexpected shapes if necessary, for now assume valid input
         # based on examples. Could return input_grid or raise error.
         print(f"Warning: Input grid shape {input_grid.shape} not (1, width). Processing first row.")
         # Proceed with the first row if possible, or adapt logic

    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Extract the first (and only expected) row
    row = output_grid[0]

    # Find the indices of the non-white block
    non_white_indices, start_index, end_index = find_non_white_block_indices(row)

    # Proceed only if a block was found
    if start_index is not None and end_index is not None:
        # Check if there are pixels strictly *between* the start and end
        # Example: [5, 5] -> start=0, end=1. No pixels between.
        # Example: [5, 5, 5] -> start=0, end=2. Pixel at index 1 is between.
        if end_index > start_index + 1:
            # Change the pixels between start_index+1 and end_index (exclusive) to white (0)
            # Slicing in numpy is exclusive of the end index, so [start+1:end] is correct
            row[start_index + 1 : end_index] = 0
            
    # The modifications were made in-place on the row extracted from output_grid,
    # so output_grid is already updated.
    return output_grid