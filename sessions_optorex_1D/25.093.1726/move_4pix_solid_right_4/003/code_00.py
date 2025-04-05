"""
Transforms a 1D input sequence by finding the first contiguous block of identical non-zero integers and shifting this block 4 positions to the right within the sequence boundaries, filling the original positions with zeros. Handles potentially nested input formats.
"""

import numpy as np

def find_non_zero_block(sequence):
    """
    Finds the first contiguous block of identical non-zero numbers in a 1D sequence.

    Args:
        sequence: A list or 1D numpy array of numbers.

    Returns:
        A tuple (value, start_index, length) if a block is found, otherwise None.
        value: The non-zero integer value of the block.
        start_index: The starting index (0-based) of the block.
        length: The number of elements in the block.
    """
    start_index = -1
    block_value = 0
    n = len(sequence)

    for i, val in enumerate(sequence):
        # Check if the element is numeric and non-zero
        is_numeric_non_zero = isinstance(val, (int, float, np.number)) and val != 0

        if is_numeric_non_zero:
            if start_index == -1: # Start of a potential new block
                start_index = i
                block_value = val
            elif val != block_value: # Found a different non-zero value, meaning the previous block ended
                # This case shouldn't happen based on problem description (only one block)
                # but handles it defensively. We assume the *first* block is the target.
                 return block_value, start_index, i - start_index
        elif start_index != -1: # End of the block because a zero (or non-numeric) was encountered
            # Found the end of the block started at start_index
            return block_value, start_index, i - start_index

    # Handle case where the block extends to the very end of the sequence
    if start_index != -1:
        return block_value, start_index, n - start_index

    # No non-zero block found in the entire sequence
    return None

def transform(input_grid):
    """
    Applies the block shifting transformation.

    Args:
        input_grid: A sequence (list, numpy array, potentially nested list/2D array with one row).

    Returns:
        A list representing the transformed sequence.
    """
    # --- Input Handling ---
    # Check for nesting (list of lists or 2D numpy array) and extract the 1D sequence
    if isinstance(input_grid, list) and len(input_grid) == 1 and isinstance(input_grid[0], (list, np.ndarray)):
        sequence = list(input_grid[0]) # Convert inner element to list
    elif isinstance(input_grid, np.ndarray) and input_grid.ndim == 2 and input_grid.shape[0] == 1:
        sequence = input_grid[0].tolist() # Convert first row to list
    elif isinstance(input_grid, (list, np.ndarray)):
         # Assume it's already a 1D sequence or convert 1D numpy array
         sequence = list(input_grid)
    else:
        # Handle unexpected input types if necessary
        raise TypeError("Input must be a list, numpy array, or a nested list/2D array representing a single sequence.")

    n = len(sequence)

    # --- Initialization ---
    # Create a new list (the output sequence) of length n, filled with zeros.
    output_sequence = [0] * n

    # --- Locate Block ---
    # Find the non-zero block in the 1D input sequence.
    block_info = find_non_zero_block(sequence)

    # --- Calculate New Position and Place Block ---
    if block_info:
        block_value, start_index, block_length = block_info

        # Calculate the new starting index for the block (shift right by 4)
        new_start_index = start_index + 4

        # Place the block into the output sequence at the new position, checking bounds
        for i in range(block_length):
            output_index = new_start_index + i
            # Ensure the index is within the valid range of the output sequence
            if 0 <= output_index < n:
                output_sequence[output_index] = block_value
            # Else: If the index is out of bounds, that part of the block is clipped (not placed)

    # --- Return Output ---
    return output_sequence