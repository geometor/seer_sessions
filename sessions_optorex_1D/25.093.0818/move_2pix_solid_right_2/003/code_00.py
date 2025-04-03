import numpy as np

"""
Identifies a contiguous block of identical non-zero integers within a sequence (list or NumPy array) of integers and shifts this block exactly two positions to the right. The output sequence maintains the same length as the input, filling positions not occupied by the shifted block with zeros.
"""

def find_non_zero_block(int_sequence):
    """
    Finds the start index, end index (exclusive), and value of the first 
    contiguous block of identical non-zero numbers in a sequence.
    
    Args:
        int_sequence: A list or NumPy array of integers.
        
    Returns:
        A tuple (start_index, end_index, value) or (None, None, None) if no block is found.
    """
    start_index = None
    block_value = None
    n = len(int_sequence)
    
    for i, val in enumerate(int_sequence):
        if val != 0:
            # Found the start of a potential block
            if start_index is None:
                start_index = i
                block_value = val
            # If we are inside a block, check if the value matches the block's value
            elif val != block_value:
                # The block ended at the previous index 'i-1', so end_index is 'i'
                return start_index, i, block_value
        # Found a zero after starting a block
        elif start_index is not None:
            # The block ends at the current index 'i'
            return start_index, i, block_value
            
    # If the loop finishes and a block was started (meaning it extends to the end)
    if start_index is not None:
        return start_index, n, block_value
        
    # No non-zero block found
    return None, None, None

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list or NumPy array of integers.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # Ensure input is treated as a list for consistent indexing
    if isinstance(input_sequence, np.ndarray):
        input_list = input_sequence.tolist()
    else:
        input_list = list(input_sequence) # Make a copy if it's already a list

    n = len(input_list)
    
    # Initialize the output list with zeros, same length as input
    output_list = [0] * n

    # Find the contiguous block of non-zero numbers in the input
    start_index, end_index, block_value = find_non_zero_block(input_list)

    # If a block was found
    if start_index is not None:
        # Define the amount to shift the block
        shift_amount = 2
        
        # Calculate the new start and end indices for the block
        new_start_index = start_index + shift_amount
        new_end_index = end_index + shift_amount
        
        # Place the block into the output list at the new position
        # Iterate through the calculated indices for the shifted block
        for i in range(new_start_index, new_end_index):
            # Ensure the index is within the bounds of the output list
            if 0 <= i < n:
                output_list[i] = block_value

    # Return the resulting output list
    return output_list