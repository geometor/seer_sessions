"""
Transforms an input sequence (potentially multi-dimensional array treated as 1D) 
containing a single contiguous block of identical non-zero integers surrounded by zeros.
The transformation shifts this non-zero block two positions to the right within a 
new sequence of the same length, filled otherwise with zeros. If the shift pushes 
part of the block beyond the sequence boundary, that part is truncated.
"""

import numpy as np

def find_non_zero_block(arr_1d):
    """
    Finds the start index, end index, and value of the first contiguous 
    block of identical non-zero numbers in a 1D NumPy array.

    Args:
        arr_1d: A 1D NumPy array of integers.

    Returns:
        A tuple (start_index, end_index, value) if a block is found,
        otherwise (-1, -1, 0).
    """
    start_index = -1
    end_index = -1
    value = 0
    in_block = False

    for i, num in enumerate(arr_1d):
        if num != 0:
            if not in_block:
                # Start of a potential block
                start_index = i
                value = num
                end_index = i # Initialize end index
                in_block = True
            elif num == value:
                # Continue the current block
                end_index = i
            else:
                # Found a different non-zero number, the first block ends here.
                # Based on examples, this implies only one block type exists.
                break 
        elif in_block:
            # Found a zero after starting a block, the block ends at the previous index
            break
            
    if start_index != -1:
        return start_index, end_index, value
    else:
        # No non-zero block found
        return -1, -1, 0

def transform(input_grid):
    # Ensure input is a NumPy array and flatten it to 1D
    input_array = np.array(input_grid).flatten()
    
    # Get the length of the 1D input array
    arr_len = len(input_array)
    
    # Initialize the output grid with zeros, matching length and type
    output_grid = np.zeros(arr_len, dtype=input_array.dtype)

    # Locate the contiguous non-zero block in the flattened input
    start_in, end_in, value = find_non_zero_block(input_array)

    # Proceed only if a valid block was found
    if start_in != -1:
        # Calculate the length of the block
        block_length = end_in - start_in + 1
        
        # Calculate the target starting position for the block in the output
        start_out = start_in + 2

        # Iterate through the elements of the block
        for i in range(block_length):
            # Calculate the target index in the output grid
            target_out_index = start_out + i
            
            # Check if the target index is within the bounds of the output grid
            if 0 <= target_out_index < arr_len:
                # If within bounds, copy the block's value to the output grid
                output_grid[target_out_index] = value
            # Else: If the target index is out of bounds, the value is truncated 
            # (implicitly not copied as output_grid remains 0 there).

    # Return the transformed grid
    return output_grid