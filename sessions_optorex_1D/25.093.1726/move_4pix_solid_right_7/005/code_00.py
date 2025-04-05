import numpy as np

"""
Identifies a contiguous block of identical non-zero integers in a potentially 2D (1xN) NumPy input array.
Flattens the input to 1D, finds the block, and shifts this block 4 positions to the right within a new 1D array of the same size, filled with zeros elsewhere.
"""

def find_non_zero_block(input_array_1d):
    """
    Finds the start index, length, and value of the first contiguous non-zero block
    in a 1D NumPy array.

    Args:
        input_array_1d: A 1D NumPy array of integers.

    Returns:
        A tuple (start_index, block_length, block_value) if a block is found,
        otherwise (None, None, None).
    """
    non_zero_indices = np.where(input_array_1d != 0)[0]

    if len(non_zero_indices) == 0:
        return None, None, None # No non-zero elements

    start_index = non_zero_indices[0]
    block_value = input_array_1d[start_index]
    block_length = 0

    # Iterate from the start index to find the end of the contiguous block
    # of the *same* non-zero value.
    for i in range(start_index, len(input_array_1d)):
        if input_array_1d[i] == block_value:
            block_length += 1
        else:
            # Stop if we hit a zero or a different non-zero number
            break 

    return start_index, block_length, block_value


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input NumPy array by shifting the non-zero block.

    Args:
        input_grid: A NumPy array (potentially 1xN or N) of integers.

    Returns:
        A 1D NumPy array with the non-zero block shifted 4 positions right.
    """
    # Ensure the input is treated as a 1D array
    input_flat = input_grid.flatten()
    n = len(input_flat)

    # Initialize the output grid as a 1D array of zeros
    output_grid = np.zeros(n, dtype=input_flat.dtype)

    # Find the contiguous block of non-zero integers in the flattened input
    start_index, block_length, block_value = find_non_zero_block(input_flat)

    # If a block was found, proceed to shift it
    if start_index is not None:
        # Calculate the new starting index for the block
        new_start_index = start_index + 4

        # Place the block into the output grid at the new position
        # Iterate for the length of the block
        for i in range(block_length):
            target_index = new_start_index + i
            # Check array bounds before writing to avoid index errors
            if target_index < n:
                output_grid[target_index] = block_value

    # Return the constructed 1D output grid
    return output_grid