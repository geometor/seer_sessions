"""
Identifies a contiguous block of identical non-zero integers in the input grid 
(assumed to have 1 row or be 1D), shifts this block 4 positions/columns to the left, 
and places it into a new grid of the same size initialized with zeros. Returns the new grid.
"""

import numpy as np

def _find_non_zero_block(int_array_1d):
    """
    Finds the start index, value, and length of the first contiguous non-zero block 
    in a 1D NumPy array or list of integers. Assumes only one such block exists.

    Args:
        int_array_1d: A 1D NumPy array or list of integers representing the sequence.

    Returns:
        A dictionary containing 'value', 'start' (0-based index), and 'length' 
        of the block, or None if no non-zero block is found.
    """
    start_index = -1
    value = 0
    length = 0
    in_block = False
    # Iterate through the array/list to find the start, value, and length of the block
    for i, digit in enumerate(int_array_1d):
        if digit != 0 and not in_block:
            # Found the start of a new non-zero block
            start_index = i
            value = digit
            length = 1
            in_block = True
        elif digit == value and in_block:
            # Continue the current block
            length += 1
        elif digit != value and in_block:
            # End of the block (since we assume only one block per input)
            break 
            
    # If no non-zero digit was found, start_index remains -1
    if start_index == -1: 
        return None
        
    return {'value': value, 'start': start_index, 'length': length}

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input 1D NumPy array or 2D (1 row) array by shifting the 
    non-zero block 4 positions to the left.

    Args:
        input_grid: A 1D NumPy array or a 2D NumPy array with shape (1, N).

    Returns:
        A new NumPy array of the same shape and type as the input, containing 
        the shifted block, with other positions filled with zeros.
        Returns a zero-filled grid if no non-zero block is found.
    """
    
    # Determine if input is 1D or 2D (with 1 row) and get dimensions/row data
    if input_grid.ndim == 2:
        # Expect shape (1, N)
        rows, n_cols = input_grid.shape 
        if rows != 1:
             # This case shouldn't occur based on problem description but good practice
             raise ValueError(f"Input grid must have exactly one row, but got {rows} rows.")
        # Extract the first (and only) row for processing
        input_row = input_grid[0] 
        is_2d = True
    elif input_grid.ndim == 1:
        # Expect shape (N,)
        n_cols = input_grid.shape[0]
        input_row = input_grid # Process directly
        is_2d = False
    else:
        raise ValueError(f"Input grid must be 1D or 2D, but got {input_grid.ndim} dimensions.")

    # Initialize the output grid with zeros, matching the input shape and type
    output_grid = np.zeros_like(input_grid)
    
    # Find the non-zero block details (value, start index, length) in the input row
    block_info = _find_non_zero_block(input_row)

    # If a non-zero block was found:
    if block_info:
        value = block_info['value']
        original_start = block_info['start']
        length = block_info['length']
        
        # Calculate the new starting position by shifting left by 4
        new_start_col = original_start - 4
        
        # Place the block into the output grid at the new position
        for i in range(length):
            # Calculate the target column index in the output grid's row/array
            target_col = new_start_col + i
            
            # Check if the target column index is within the valid bounds (0 to n_cols-1)
            if 0 <= target_col < n_cols: 
                 # Assign value based on whether original was 1D or 2D
                 if is_2d:
                     output_grid[0, target_col] = value
                 else: # ndim == 1
                     output_grid[target_col] = value

    # Return the modified grid containing the shifted block (or all zeros if no block found)
    return output_grid