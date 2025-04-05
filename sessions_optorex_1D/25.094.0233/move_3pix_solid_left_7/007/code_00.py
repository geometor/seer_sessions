"""
Transforms an input sequence of integers by finding the first contiguous block
of identical non-zero numbers and shifting this block exactly 3 positions to
the left to create the output sequence. The sequence length and the block's
value and length remain constant. Positions outside the shifted block in the
output are filled with zeros.
"""

import numpy as np

def find_block(sequence):
    """
    Finds the first contiguous block of identical non-zero numbers in a sequence.

    Args:
        sequence (np.array): The input sequence of numbers.

    Returns:
        tuple: (start_index, value, length) of the block, or (None, None, None)
               if no such block is found.
    """
    start_index = None
    value = None
    length = 0
    n = len(sequence)
    i = 0
    # Iterate through the sequence to find the start of the first non-zero block
    while i < n:
        # Check if the current element is non-zero
        if sequence[i] != 0:
            # Record the start index and value of the block
            start_index = i
            value = sequence[i]
            length = 1
            # Count the length of the contiguous block of the same value
            j = i + 1
            while j < n and sequence[j] == value:
                length += 1
                j += 1
            # Found the first block, so break the outer loop
            break
        # Move to the next element if the current one is zero
        i += 1

    # Return the found block properties or None if no block was found
    if start_index is not None:
        return start_index, value, length
    else:
        return None, None, None

def transform(input_grid):
    """
    Applies the block-shifting transformation to the input sequence.

    Args:
        input_grid (list or np.array): The input sequence of integers.

    Returns:
        np.array: The transformed sequence as a NumPy array.
    """
    # Ensure input is treated as a NumPy array for consistent handling and output type
    input_sequence = np.array(input_grid, dtype=int)
    n = len(input_sequence)

    # Initialize output_grid as a NumPy array of zeros with the same length
    output_grid = np.zeros(n, dtype=int)

    # Scan the input sequence to find the non-zero block properties
    start_index, value, length = find_block(input_sequence)

    # Check if a block was successfully found
    if start_index is not None:
        # Calculate the target starting index for the block in the output
        # by shifting left by 3 positions
        output_start_index = start_index - 3

        # Iterate through the elements of the identified block
        for i in range(length):
            # Calculate the index where the current block element should be placed
            current_output_index = output_start_index + i

            # Check if this target index is within the valid bounds of the output grid
            if 0 <= current_output_index < n:
                # If valid, place the block's value at this position in the output grid
                output_grid[current_output_index] = value
            # If the index is out of bounds, the element is effectively dropped (remains 0)

    # Return the resulting output grid
    return output_grid