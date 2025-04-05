```python
"""
Identifies a contiguous block of identical non-zero integers in a 1D input NumPy array.
Shifts this block 4 positions to the left, placing it into a new array of the same size initialized with zeros.
Returns the new array containing the shifted block.
"""

import numpy as np

def _find_non_zero_block(int_list):
    """
    Finds the start index, value, and length of the first contiguous non-zero block 
    in a list of integers. Returns None if no non-zero block is found.
    
    Args:
        int_list: A list of integers representing the input sequence.

    Returns:
        A dictionary containing 'value', 'start', and 'length' of the block,
        or None if no non-zero block is found.
    """
    start_index = -1
    value = 0
    length = 0
    in_block = False
    # Iterate through the list to find the start, value, and length of the block
    for i, digit in enumerate(int_list):
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
            # End of the block (assuming only one block per input)
            break 
            
    # If no non-zero digit was found, start_index remains -1
    if start_index == -1: 
        return None
        
    return {'value': value, 'start': start_index, 'length': length}

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input 1D NumPy array by shifting the non-zero block.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A new 1D NumPy array of the same size containing the shifted block,
        with other positions filled with zeros.
    """
    
    # Get the size of the input grid
    n = input_grid.shape[0]
    
    # Initialize the output grid with zeros, matching the input size and type
    output_grid = np.zeros_like(input_grid)
    
    # Convert NumPy array to list to use the helper function
    input_list = input_grid.tolist()

    # Find the non-zero block details (value, start index, length)
    block_info = _find_non_zero_block(input_list)

    # If a non-zero block was found:
    if block_info:
        value = block_info['value']
        original_start = block_info['start']
        length = block_info['length']
        
        # Calculate the new starting position by shifting left by 4
        new_start = original_start - 4
        
        # Place the block into the output grid at the new position
        for i in range(length):
            # Calculate the target index in the output grid
            target_idx = new_start + i
            
            # Ensure the target index is within the valid bounds of the grid (0 to n-1)
            if 0 <= target_idx < n: 
                 output_grid[target_idx] = value

    # Return the modified grid containing the shifted block
    return output_grid
```