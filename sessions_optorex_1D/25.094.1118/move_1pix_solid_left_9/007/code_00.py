"""
Identifies a single, contiguous block of identical non-zero digits within a 1D 
NumPy array. Shifts this block one position to the left, maintaining the 
original array length by padding with zeros. Assumes the input contains at most 
one such block and that if a block exists and is shifted, its initial start 
index is greater than 0. If no valid block is found, or if the block starts 
at index 0, an array of zeros is returned.
"""

import numpy as np

def find_non_zero_block_indices(arr):
    """
    Finds the start index, end index (exclusive), and value of the 
    first contiguous block of identical non-zero digits in a NumPy array.

    Args:
        arr: A 1D NumPy array of integers.

    Returns:
        A tuple (start_index, end_index, value) if a block is found,
        otherwise returns (None, None, None). Returns None if multiple blocks
        or non-contiguous non-zero elements are found.
    """
    # Find indices of all non-zero elements
    non_zero_indices = np.where(arr != 0)[0]

    # If no non-zero elements exist, no block can be found
    if len(non_zero_indices) == 0:
        return None, None, None

    # Determine the potential start index and the value of the block
    start_index = non_zero_indices[0]
    value = arr[start_index]
    
    # Verify that the non-zero elements form a single contiguous block
    # and all elements within that block have the same value.
    is_single_contiguous_block = True
    for i in range(len(non_zero_indices)):
        # Check for contiguity: current index should equal start_index + offset
        if non_zero_indices[i] != start_index + i:
            is_single_contiguous_block = False
            break
        # Check for homogeneity: current element value should match the first non-zero value
        if arr[non_zero_indices[i]] != value:
            is_single_contiguous_block = False
            break
            
    # If it forms a valid single contiguous block of identical values
    if is_single_contiguous_block:
        # Calculate the end index (exclusive)
        end_index = start_index + len(non_zero_indices)
        return start_index, end_index, value
    else:
        # If not a single contiguous block of the same value, return None tuple
        return None, None, None

def transform(input_grid):
    """
    Applies the left-shift transformation to the non-zero block in the input grid.

    Args:
        input_grid: A list or 1D NumPy array representing the input sequence.

    Returns:
        A 1D NumPy array representing the transformed sequence.
    """
    # Ensure input is a NumPy array for efficient processing
    input_arr = np.array(input_grid)
    
    # Get the size of the input array
    n = len(input_arr)
    
    # Initialize output_grid as a NumPy array of zeros with the same shape as input_arr
    output_grid = np.zeros_like(input_arr)

    # Find the single, contiguous, homogeneous block of non-zero digits
    start_index, end_index, block_value = find_non_zero_block_indices(input_arr)

    # Check if a valid block was found and if its start index allows for a left shift (start > 0)
    if start_index is not None and start_index > 0:
        # Calculate the new start index (shifted one position left)
        new_start_index = start_index - 1
        # Calculate the new end index (shifted one position left)
        new_end_index = end_index - 1 

        # Place the block's value into the output grid at the new, shifted position
        # Use NumPy slicing for efficient array modification
        output_grid[new_start_index:new_end_index] = block_value
        
    # If no block is found (start_index is None), or if the block starts at index 0 (start_index == 0),
    # the output_grid remains all zeros as initialized.

    return output_grid