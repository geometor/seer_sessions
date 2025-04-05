"""
Transforms an input array of 12 integers by finding a single contiguous block of 
identical non-zero digits and shifting this block 3 positions to the left. 
The value and length of the block are preserved. The remaining positions in the 
output array are filled with zeros. Assumes input is a NumPy array.
"""

import numpy as np

def find_non_zero_block(input_array):
    """
    Finds the start index, value, and length of the first contiguous block 
    of non-zero identical elements in the input array.

    Args:
        input_array (np.ndarray): The 1D input array.

    Returns:
        tuple: (start_index, block_value, block_length) or (None, None, None) if no block found.
    """
    non_zero_indices = np.where(input_array != 0)[0]
    
    if len(non_zero_indices) == 0:
        return None, None, None  # No non-zero elements found

    start_index = non_zero_indices[0]
    block_value = input_array[start_index]
    block_length = 0
    
    # Verify contiguity and determine length (more robust than just len(non_zero_indices))
    for i in range(start_index, len(input_array)):
        if input_array[i] == block_value:
            block_length += 1
        else:
            break # End of the block (or unexpected value)
            
    # Check if the found non_zero_indices match the expected contiguous block length
    if block_length != len(non_zero_indices) or non_zero_indices[-1] != start_index + block_length -1 :
       # This condition handles cases where non-zeros might not be contiguous or identical,
       # although the problem description implies they always are.
       # For this specific problem based on examples, we can perhaps simplify, 
       # but this is more robust. We'll proceed assuming contiguity based on examples.
       block_length = len(non_zero_indices) # Revert to simple length based on examples

    return start_index, block_value, block_length

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the left shift transformation to the non-zero block.

    Args:
        input_grid (np.ndarray): A 1D NumPy array of 12 integers.

    Returns:
        np.ndarray: The transformed 1D NumPy array.
    """
    n = len(input_grid)
    # Initialize output_grid with zeros
    output_grid = np.zeros_like(input_grid)

    # Find the non-zero block details
    start_index, block_value, block_length = find_non_zero_block(input_grid)

    # If a block was found
    if start_index is not None:
        # Calculate the new starting index after shifting left by 3
        new_start_index = start_index - 3

        # Place the block into the output grid at the new position
        for i in range(block_length):
            output_index = new_start_index + i
            # Check array bounds before writing
            if 0 <= output_index < n:
                output_grid[output_index] = block_value

    return output_grid