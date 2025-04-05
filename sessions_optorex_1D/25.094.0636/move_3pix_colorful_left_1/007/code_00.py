"""
Transforms a 1D NumPy integer array by identifying the contiguous block of non-zero
elements, shifting this block 3 positions to the left (clamping the start index at 0),
and placing it into a new array of the same shape and dtype, padded with zeros at
the remaining positions, primarily at the end.
"""

import numpy as np

def find_contiguous_non_zero_block_bounds(arr: np.ndarray) -> tuple[int, int]:
    """
    Finds the start and end indices of the contiguous block of non-zero numbers
    in a 1D NumPy array.

    Args:
        arr: A 1D NumPy array of integers.

    Returns:
        A tuple (start_index, end_index). Returns (-1, -1) if no non-zero numbers
        are found. Assumes non-zero elements form a single contiguous block based
        on problem examples.
    """
    # Find indices of all non-zero elements
    non_zero_indices = np.nonzero(arr)[0]
    
    # If no non-zero elements, return (-1, -1)
    if len(non_zero_indices) == 0:
        return -1, -1 

    # The start index is the first non-zero index
    start_index = non_zero_indices[0]
    # The end index is the last non-zero index
    end_index = non_zero_indices[-1]

    return start_index, end_index


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.
    """
    # Get the shape and data type of the input grid
    n = input_grid.shape[0]
    dtype = input_grid.dtype

    # Initialize the output grid with zeros, matching input shape and type
    output_grid = np.zeros_like(input_grid)

    # Find the start and end indices of the non-zero block in the input
    start_index, end_index = find_contiguous_non_zero_block_bounds(input_grid)

    # If no non-zero block is found (input is all zeros), return the zero-filled grid
    if start_index == -1:
        return output_grid

    # Extract the non-zero block from the input grid
    non_zero_block = input_grid[start_index : end_index + 1]
    block_len = len(non_zero_block)

    # Define the shift amount
    shift_amount = 3

    # Calculate the target starting index for the block in the output grid
    # Shift left by the specified amount, but clamp at index 0 (cannot go negative)
    new_start_index = max(0, start_index - shift_amount)

    # Calculate the target ending index (exclusive) for placing the block
    # Ensure the block placement does not exceed the grid's bounds
    new_end_index_exclusive = min(n, new_start_index + block_len)

    # Determine the actual length of the block segment that fits into the output grid
    # This handles potential truncation if the shifted block hits the end boundary,
    # though not observed in the examples.
    place_len = new_end_index_exclusive - new_start_index

    # Place the non-zero block (or the part that fits) into the output grid
    # at the calculated new position.
    if place_len > 0: # Only place if there's space and the block has length
        output_grid[new_start_index : new_end_index_exclusive] = non_zero_block[:place_len]

    # The rest of the output_grid remains zeros as initialized.
    return output_grid