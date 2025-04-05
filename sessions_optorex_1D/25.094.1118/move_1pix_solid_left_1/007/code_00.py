"""
Transforms a 1D numpy array of integers by finding the first contiguous block 
of identical non-zero digits and shifting this block one position to the left. 
The array length remains constant, with zeros filling positions not occupied 
by the shifted block.
"""

import numpy as np

def find_first_block_np(data: np.ndarray):
    """
    Finds the start index, end index (exclusive), and value of the first 
    contiguous block of identical non-zero numbers in a NumPy array.

    Args:
        data: A 1D NumPy array of numbers.

    Returns:
        A tuple (start_index, end_index, value) if a block is found,
        otherwise (None, None, None).
    """
    # Step 3: Search input_array for the first non-zero element.
    non_zero_indices = np.nonzero(data)[0]

    # Step 4: If no non-zero element is found, signal this.
    if len(non_zero_indices) == 0:
        return None, None, None

    # Step 5: If a non-zero element is found, record its index and value.
    start_index = non_zero_indices[0]
    block_value = data[start_index]
    
    # Step 6: Determine the end_index of the contiguous block.
    end_index = start_index + 1
    n = len(data)
    while end_index < n and data[end_index] == block_value:
        end_index += 1
        
    return start_index, end_index, block_value


def transform(input_grid: np.ndarray) -> np.ndarray:
    # Step 1: Accept the input 1D integer array (input_grid) - implicit in function signature.

    # Step 2: Initialize an output_array of the same size as input_array and fill it with zeros.
    output_grid = np.zeros_like(input_grid)

    # Steps 3-6: Find the details of the first non-zero block using the helper function.
    start_index, end_index, block_value = find_first_block_np(input_grid)

    # Step 4 (cont.): If no block is found, return the initialized (all zero) output array.
    if start_index is None:
        return output_grid 

    # Step 7: Calculate the target position for the block in the output_array.
    new_start_index = start_index - 1
    new_end_index = end_index - 1 # Block length remains the same, so end index shifts too.

    # Step 8: Determine the actual range to modify in output_array, respecting boundaries.
    actual_slice_start = max(0, new_start_index)
    # Ensure the end index doesn't exceed the array length
    actual_slice_end = min(len(output_grid), new_end_index) 

    # Step 9: If the target slice is valid and has non-zero length, assign the block_value.
    if actual_slice_start < actual_slice_end:
         # Assign the block value to the calculated slice in the output grid
         output_grid[actual_slice_start:actual_slice_end] = block_value

    # Step 10: Return the modified output_array.
    return output_grid