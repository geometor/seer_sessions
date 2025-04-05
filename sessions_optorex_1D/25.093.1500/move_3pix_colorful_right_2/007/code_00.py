"""
Shift the single contiguous block of non-zero numbers within a 1D numerical 
array 3 positions to the right, maintaining array length by padding with zeros. 
If the input contains only zeros, return it unchanged.
"""

import numpy as np

def find_contiguous_non_zero_block(arr):
    """
    Finds the start index, end index, and values of the first contiguous 
    block of non-zero numbers in a NumPy array. Assumes only one such block exists.

    Args:
        arr: A 1D NumPy array of numbers.

    Returns:
        A tuple (start_index, end_index, block_values) if a contiguous block
        is found, otherwise (None, None, None).
    """
    # Find indices where the element is not zero
    non_zero_indices = np.where(arr != 0)[0]

    # If there are no non-zero elements, return None for all values
    if len(non_zero_indices) == 0:
        return None, None, None

    # Determine the start and end index of the non-zero sequence
    start_index = non_zero_indices[0]
    end_index = non_zero_indices[-1]

    # Extract the block of non-zero values
    # Assuming contiguity based on problem description and examples
    block_values = arr[start_index : end_index + 1]

    return start_index, end_index, block_values


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input 1D NumPy array by shifting the non-zero block.

    Args:
        input_grid: A 1D NumPy array of numbers.

    Returns:
        A 1D NumPy array with the non-zero block shifted, or a copy of the 
        original array if no non-zero block exists.
    """
    # 1. Find the contiguous non-zero block in the input array
    start_idx, end_idx, block_values = find_contiguous_non_zero_block(input_grid)

    # 2. Handle the case where no non-zero block is found (all zeros)
    if start_idx is None:
        return np.copy(input_grid) # Return a copy to avoid modifying original if it's passed elsewhere

    # 3. Define the shift amount
    shift_amount = 3
    n = len(input_grid) # Get the length of the input array

    # 4. Create the output grid, initialized with zeros, same shape and type as input
    output_grid = np.zeros_like(input_grid)

    # 5. Calculate the new starting position for the block
    new_start_idx = start_idx + shift_amount

    # 6. Determine the slice of the block that fits into the output grid
    # Calculate how many elements from the block can be copied
    num_elements_in_block = len(block_values)
    # Calculate the end index in the output grid *if* the whole block fit
    potential_end_idx_output = new_start_idx + num_elements_in_block
    # Calculate how many elements actually fit within the grid bounds (n)
    num_elements_to_copy = max(0, min(num_elements_in_block, n - new_start_idx))

    # 7. Copy the relevant part of the non-zero block to the new position
    if num_elements_to_copy > 0:
        # Slice the block_values to get only the elements that will fit
        block_to_copy = block_values[:num_elements_to_copy]
        # Define the target slice in the output grid
        output_slice_start = new_start_idx
        output_slice_end = new_start_idx + num_elements_to_copy
        # Assign the sliced block to the target slice in the output grid
        output_grid[output_slice_start:output_slice_end] = block_to_copy

    # 8. Return the transformed grid
    return output_grid