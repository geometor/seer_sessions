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
    # Find indices of all non-zero elements
    non_zero_indices = np.nonzero(data)[0]

    # If no non-zero element found, no block exists
    if len(non_zero_indices) == 0:
        return None, None, None

    # The start index is the first non-zero index
    start_index = non_zero_indices[0]
    block_value = data[start_index]
    
    # Find the end of the block (index after the last element)
    end_index = start_index + 1
    n = len(data)
    while end_index < n and data[end_index] == block_value:
        end_index += 1
        
    # This logic implicitly handles finding the *first* block because it
    # starts searching for the end only from the *first* non-zero index found.

    return start_index, end_index, block_value


def transform(input_grid: np.ndarray) -> np.ndarray:
    # 1. Receive the input 1D integer array (input_grid)

    # 2. Initialize an output array of the same length as the input array, filled with zeros.
    output_grid = np.zeros_like(input_grid)

    # 3. & 4. & 5. & 6. Find the details of the first non-zero block.
    start_index, end_index, block_value = find_first_block_np(input_grid)

    # If no block is found, return the initialized (all zero) output array.
    if start_index is None:
        return output_grid # Step 4 completion

    # 7. Calculate the new starting position for the block (shifted left by 1)
    new_start_index = start_index - 1
    
    # 8. Calculate the new end position for the block
    new_end_index = end_index - 1 # block length remains the same

    # 9. Fill the elements of the output array with the block value at the new position.
    # Ensure the target indices are within the bounds of the array.
    # Python slicing handles the start boundary correctly (e.g., if new_start_index is -1, it's ignored).
    # We only need to ensure new_start_index is less than the array length for the slice to be potentially valid.
    if new_start_index < len(output_grid):
        # Calculate the actual start for slicing (must be >= 0)
        actual_slice_start = max(0, new_start_index)
        # Calculate the actual end for slicing (must be <= length)
        actual_slice_end = min(len(output_grid), new_end_index)

        # Only assign if the slice is valid (start < end)
        if actual_slice_start < actual_slice_end:
             output_grid[actual_slice_start:actual_slice_end] = block_value

    # 10. Return the modified output array.
    return output_grid