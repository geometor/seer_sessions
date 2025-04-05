import numpy as np
import math
import collections

"""
The transformation rule shifts a contiguous block of identical non-zero integers within a sequence (represented as a 1D NumPy array of length 12) three positions to the left. Zeros fill the vacated positions, and any part of the block shifted beyond the left boundary (index 0) is truncated.
"""

def find_non_zero_block(int_array):
    """
    Finds the contiguous block of identical non-zero numbers in a 1D numpy array.

    Args:
        int_array: A 1D numpy array of integers.

    Returns:
        A tuple containing:
        - block_value (int): The non-zero value of the block (0 if no block found).
        - start_index (int): The starting index of the block (-1 if no block found).
        - block_length (int): The length of the block (0 if no block found).
    """
    start_index = -1
    block_value = 0
    block_length = 0
    
    # Iterate through the array to find the block
    for i, val in enumerate(int_array):
        if val != 0:
            # Found the start of a potential block
            if start_index == -1:
                start_index = i
                block_value = val
                block_length = 1
            # Continuing the identified block
            elif val == block_value:
                block_length += 1
            # Encountered a different non-zero value (shouldn't happen per constraints)
            # or a zero after the block started. Stop searching.
            else: 
                break 
        elif start_index != -1:
            # Found a zero after the block started, so the block ends here
            break
            
    # Return block details or default values if no block was found
    if start_index != -1:
        return block_value, start_index, block_length
    else:
        return 0, -1, 0

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Shifts a contiguous block of identical non-zero numbers 3 positions 
    to the left within a 1D NumPy array of 12 integers.

    Args:
        input_grid: A 1D NumPy array representing the input sequence.

    Returns:
        A 1D NumPy array representing the transformed sequence.
    """
    
    # Define sequence length based on input or constraints
    sequence_length = input_grid.shape[0] if input_grid is not None else 12
    if sequence_length != 12:
        # Handle potential mismatch, although examples are fixed at 12
        # For robustness, could raise an error or adapt, but sticking to 12 based on examples
        sequence_length = 12 

    # Initialize the output grid (NumPy array) with zeros
    output_grid = np.zeros(sequence_length, dtype=int)

    # Find the non-zero block in the input grid
    block_value, start_index, block_length = find_non_zero_block(input_grid)

    # If a non-zero block was found, proceed with the shift
    if block_value != 0:
        # Define the shift amount
        shift_amount = 3
        
        # Calculate the target start index after shifting left
        new_start_index = start_index - shift_amount

        # Place the block into the output grid, handling boundary conditions
        for i in range(block_length):
            # Calculate the target index for the current element of the block
            target_index = new_start_index + i
            
            # Check if the target index is within the valid bounds of the output grid
            if 0 <= target_index < sequence_length:
                # Assign the block's value to the calculated position in the output grid
                output_grid[target_index] = block_value

    # Return the resulting output grid
    return output_grid