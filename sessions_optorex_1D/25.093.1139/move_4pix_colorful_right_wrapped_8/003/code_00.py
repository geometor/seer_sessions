"""
Transforms an input list of 12 integers by dividing it into three consecutive blocks of 4 elements each and rearranging these blocks. The output list is formed by concatenating the blocks in the order: Block 3 (indices 8-11), Block 1 (indices 0-3), and Block 2 (indices 4-7).
"""

import numpy as np # Import numpy, though basic list operations are sufficient

def transform(input_list):
    """
    Rearranges a list of 12 integers by blocks.

    Args:
        input_list: A list or numpy array of 12 integers.

    Returns:
        A list of 12 integers rearranged according to the rule: Block 3, Block 1, Block 2.
    """
    # Define block size (optional, but good for clarity)
    block_size = 4
    
    # Ensure input is treated as a list for consistent slicing/concatenation
    # This handles cases where the input might be a numpy array
    if isinstance(input_list, np.ndarray):
        input_list = input_list.tolist()
        
    # Check if the input list has the expected length
    if len(input_list) != 12:
        # Handle error case, though based on problem description, length is fixed
        # For this task, we might assume valid input, but adding a check is robust
        raise ValueError("Input list must contain exactly 12 elements.")

    # Extract the three blocks using list slicing
    # Block 1: elements at indices 0 through 3
    block_1 = input_list[0 * block_size : 1 * block_size] 
    # Block 2: elements at indices 4 through 7
    block_2 = input_list[1 * block_size : 2 * block_size] 
    # Block 3: elements at indices 8 through 11
    block_3 = input_list[2 * block_size : 3 * block_size] 

    # Construct the output list by concatenating the blocks in the order 3, 1, 2
    output_list = block_3 + block_1 + block_2

    # Return the rearranged list
    return output_list