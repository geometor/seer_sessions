"""
Transforms a 1D input grid (represented as a 2D NumPy array with shape (1, N)) 
of integers by finding the first contiguous block of non-zero numbers in the 
first row and shifting it two column positions to the left. The shift is 
clamped at the beginning of the row (column index 0). The grid shape is 
maintained, and vacated positions are filled with zeros. If no non-zero 
block exists, a grid of zeros of the same shape is returned.
"""

import numpy as np
import math # Retained for max, although standard max works

def find_non_zero_block_in_row(grid_row):
    """
    Finds the start column index, end column index, and content of the first 
    contiguous block of non-zero integers in a 1D NumPy array (grid row).

    Args:
        grid_row: A 1D NumPy array of integers representing a row from the grid.

    Returns:
        A tuple (start_col_index, end_col_index, block_content).
        Returns (-1, -1, np.array([], dtype=int)) if no non-zero block is found.
    """
    # Find indices of all non-zero elements in the row
    non_zero_indices = np.nonzero(grid_row)[0]

    # If no non-zero elements exist, return indication of no block found
    if len(non_zero_indices) == 0:
        return -1, -1, np.array([], dtype=int) # Use -1 to indicate not found

    # The start index is the first non-zero index found
    start_col_index = non_zero_indices[0]

    # Find the end index of the first *contiguous* block
    end_col_index = start_col_index
    for i in range(1, len(non_zero_indices)):
        # Check if the current non-zero index is consecutive to the previous one
        if non_zero_indices[i] == non_zero_indices[i-1] + 1:
            end_col_index = non_zero_indices[i] # Extend the block
        else:
            # The block is broken, stop searching for this block's end
            break

    # Extract the block content using slicing based on found indices
    block_content = grid_row[start_col_index : end_col_index + 1]

    return start_col_index, end_col_index, block_content


def transform(input_grid):
    """
    Applies the left-shift transformation to the input grid.

    Args:
        input_grid: A 2D NumPy array (expected shape (1, N)) containing integers.

    Returns:
        A 2D NumPy array containing the transformed integers, with the same shape
        as the input_grid.
    """
    # Ensure input is a NumPy array and get its shape
    input_grid_np = np.array(input_grid)
    if input_grid_np.ndim != 2 or input_grid_np.shape[0] != 1:
         # Handle unexpected input shapes if necessary, maybe raise error
         # For now, assume correct shape (1, N) based on examples
         pass
         
    original_shape = input_grid_np.shape
    num_cols = original_shape[1]

    # 1. Initialize output_grid with zeros, matching input shape and type
    output_grid = np.zeros(original_shape, dtype=input_grid_np.dtype)

    # 2. Extract the first (and only) row
    input_row = input_grid_np[0]

    # 3. Find the first contiguous block of non-zero numbers in the row
    start_col_index, end_col_index, non_zero_block = find_non_zero_block_in_row(input_row)

    # 4. If a non-zero block was found, proceed with transformation
    if start_col_index != -1: # Check if a block was found
        # 5. Calculate the new starting column index for the block
        # Shift left by 2, ensuring it doesn't go below column index 0
        new_start_col_index = max(0, start_col_index - 2)

        # 6. Get the length of the block
        block_length = len(non_zero_block)

        # 7. Calculate the end column index for placing the block in the output grid
        # Ensure the placement doesn't exceed the number of columns
        new_end_col_index = min(new_start_col_index + block_length, num_cols)
        
        # 8. Calculate the length of the block part that actually fits
        # This handles cases where the shifted block might partially go off the right edge,
        # although with fixed length, this mainly ensures correct slicing.
        actual_block_length_to_place = new_end_col_index - new_start_col_index

        # 9. Place the (potentially truncated) non-zero block into the output grid's first row
        if actual_block_length_to_place > 0:
             output_grid[0, new_start_col_index : new_end_col_index] = non_zero_block[:actual_block_length_to_place]

    # 10. Return the transformed grid
    # If no block was found, this returns the grid of zeros initialized earlier.
    return output_grid