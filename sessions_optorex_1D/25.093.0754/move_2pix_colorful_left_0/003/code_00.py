"""
Transforms an input 2D NumPy array (with one row) by identifying the 
contiguous block of numbers starting from the first non-zero element and 
ending with the last non-zero element in the row. This block is then 
shifted two positions to the left in the output row. Positions outside 
the shifted block are filled with zeros. The output has the same shape 
as the input.
"""

import numpy as np

def transform(input_grid):
    """
    Identifies the content block bounded by the first and last non-zero 
    elements in the input grid's single row and shifts this block two 
    positions to the left.

    Args:
        input_grid (np.ndarray): A 2D NumPy array with shape (1, N).

    Returns:
        np.ndarray: A 2D NumPy array with shape (1, N) containing the 
                    transformed row.
    """
    # Ensure input is a numpy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)

    # Check if input_grid is unexpectedly empty or not 2D
    if input_grid.ndim != 2 or input_grid.shape[0] != 1 or input_grid.shape[1] == 0:
         # Return an empty array or handle error appropriately
         # For this task, assuming valid input shape (1, N) based on examples
         # If N=0, return shape (1,0)
         if input_grid.shape[1] == 0:
             return np.zeros((1,0), dtype=input_grid.dtype)
         else:
             # Or raise an error if shape is fundamentally wrong
             raise ValueError("Input grid must be a 2D numpy array with shape (1, N)")

    # Extract the first (and only) row
    input_row = input_grid[0, :]
    n = input_row.size

    # Initialize the output row with zeros
    output_row = np.zeros(n, dtype=input_row.dtype)

    # Find the indices of non-zero elements
    non_zero_indices = np.nonzero(input_row)[0] # np.nonzero returns a tuple of arrays

    # Check if there are any non-zero elements
    if non_zero_indices.size == 0:
        # If all zeros, return the grid of zeros (reshaped)
        return output_row.reshape(1, n)

    # Find the index of the first and last non-zero elements
    first_nz_index = non_zero_indices[0]
    last_nz_index = non_zero_indices[-1]

    # Extract the content block
    content_block = input_row[first_nz_index : last_nz_index + 1]

    # Calculate the target starting index (shift left by 2)
    target_start_index = first_nz_index - 2

    # Determine the actual slice ranges for copying, handling negative target_start_index
    
    # Start index in the output row (cannot be less than 0)
    out_start = max(0, target_start_index)
    
    # Corresponding start index in the content block
    # If target_start_index is -1, block_start is 1. If -2, block_start is 2. etc.
    block_start = max(0, -target_start_index) 
    
    # Number of elements to actually copy (limited by block length and output length)
    # Length of the part of the block that *can* be placed
    block_len_to_copy = content_block.size - block_start 
    # Length of the available space in the output row
    output_space_available = n - out_start
    
    num_elements_to_copy = min(block_len_to_copy, output_space_available)

    # End index (exclusive) in the output row
    out_end = out_start + num_elements_to_copy
    
    # End index (exclusive) in the content block
    block_end = block_start + num_elements_to_copy

    # Place the relevant part of the content block into the output row
    if num_elements_to_copy > 0: # Ensure there's something to copy
        output_row[out_start : out_end] = content_block[block_start : block_end]

    # Reshape the output row back to a 2D grid (1 row) and return
    output_grid = output_row.reshape(1, n)
    
    return output_grid