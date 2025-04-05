"""
Transforms an input sequence of 12 integers by finding a single contiguous block of 
identical non-zero digits and shifting this block 3 positions to the left. 
The value and length of the block are preserved. The remaining positions in the 
output sequence are filled with zeros. Elements shifted past the beginning of the 
sequence (index 0) are discarded.
"""

import numpy as np

def find_non_zero_block(input_array):
    """
    Finds the start index, value, and length of the first contiguous block 
    of non-zero identical elements in the input array.

    Args:
        input_array (np.ndarray): The 1D input array.

    Returns:
        tuple: (start_index, block_value, block_length) or (None, None, None) 
               if no block found or if the input constraints are violated.
    """
    # Find indices of all non-zero elements
    non_zero_indices = np.where(input_array != 0)[0]
    
    # If no non-zero elements, return None
    if len(non_zero_indices) == 0:
        return None, None, None

    # The block starts at the first non-zero index
    start_index = non_zero_indices[0]
    # The value of the block is the value at the start index
    block_value = input_array[start_index]
    
    # Determine the block length by checking for contiguity and identical value
    block_length = 0
    for i in range(start_index, len(input_array)):
        if input_array[i] == block_value:
            block_length += 1
        elif input_array[i] == 0: # End of block if we hit a zero
            break
        else: # If we hit a different non-zero value, constraints are violated
              # Based on examples, this shouldn't happen. Return None to be safe.
              # print(f"Warning: Found unexpected non-zero value {input_array[i]} after block of {block_value}")
              return None, None, None # Or handle error as appropriate

    # Simple check: ensure the number of non-zero elements matches the block length found
    if len(non_zero_indices) != block_length:
        # This implies non-contiguous non-zero elements or other violations
        # print(f"Warning: Number of non-zero indices ({len(non_zero_indices)}) doesn't match calculated block length ({block_length})")
        return None, None, None # Constraints violated

    return start_index, block_value, block_length

def transform(input_grid):
    """
    Applies the left shift transformation to the non-zero block.

    Args:
        input_grid (list or np.ndarray): A sequence of 12 integers.

    Returns:
        np.ndarray: The transformed 1D NumPy array.
    """
    # Ensure input is a NumPy array for consistent operations
    input_array = np.array(input_grid)
    n = len(input_array) # Should be 12 based on examples
    
    # 1. Create a new output sequence of 12 zeros.
    output_grid = np.zeros_like(input_array)

    # 2. Find the index of the first non-zero element, its value, and block length.
    block_details = find_non_zero_block(input_array)

    # If no block is found (or constraints violated), return the sequence of zeros.
    if block_details is None or block_details[0] is None:
        return output_grid
        
    start_index, block_value, block_length = block_details
    
    # 5. Calculate the target start index for the block in the output sequence.
    new_start_index = start_index - 3

    # 6. Iterate through the block length and place elements in the output grid.
    for i in range(block_length):
        # a. Calculate the target index in the output sequence.
        output_index = new_start_index + i
        
        # b. If target_index is within the valid range, place the value.
        #    Elements shifted beyond index 0 (output_index < 0) are ignored.
        if 0 <= output_index < n:
            output_grid[output_index] = block_value

    # 7. Return the modified output sequence.
    return output_grid