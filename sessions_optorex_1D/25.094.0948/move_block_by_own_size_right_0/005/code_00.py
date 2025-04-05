"""
Transforms an input 1D sequence (list or NumPy array) containing a single 
contiguous block of identical non-zero integers surrounded by zeros. 
The transformation shifts this block to the right by a distance equal to its length. 
Positions originally occupied by the block become zeros in the output. 
Elements shifted beyond the sequence boundary are discarded.
The output sequence has the same length as the input.
"""

import numpy as np

def find_block_properties(input_seq):
    """
    Identifies the contiguous block of identical non-zero integers.

    Args:
        input_seq: A 1D NumPy array of integers.

    Returns:
        A tuple (start_index, block_length, block_value) if a valid block 
        is found, otherwise returns (-1, 0, 0).
        - start_index: The starting index of the block.
        - block_length: The number of elements in the block.
        - block_value: The integer value of the elements in the block.
    """
    # Find indices of all non-zero elements
    non_zero_indices = np.where(input_seq != 0)[0]

    # If no non-zero elements, return failure indicator
    if len(non_zero_indices) == 0:
        return -1, 0, 0

    # Determine potential block boundaries and value from non-zero indices
    start_index = non_zero_indices[0]
    end_index = non_zero_indices[-1]
    block_value = input_seq[start_index]

    # Calculate the span covered by the potential block
    span_length = end_index - start_index + 1

    # Check 1: Contiguity
    # The number of non-zero elements found must equal the span length.
    # This ensures there are no zeros within the identified block range.
    is_contiguous = (len(non_zero_indices) == span_length)

    if not is_contiguous:
        # print(f"Debug: Non-contiguous non-zero elements found in {input_seq}")
        return -1, 0, 0 # Invalid block

    # Check 2: Uniformity
    # All elements within the identified span [start_index, end_index] must have the same value.
    # Slicing includes the end_index
    is_uniform = np.all(input_seq[start_index : end_index + 1] == block_value)

    if not is_uniform:
        # print(f"Debug: Block is not uniform in {input_seq}")
        return -1, 0, 0 # Invalid block
        
    # If both checks pass, it's a valid block. The length is the span length.
    block_length = span_length
    return start_index, block_length, block_value


def transform(input_grid):
    """
    Applies the block shifting transformation to the input grid.

    Args:
        input_grid: A list or 1D NumPy array representing the input sequence.

    Returns:
        A 1D NumPy array representing the transformed sequence.
    """
    # Ensure input is a NumPy array for efficient operations
    input_seq = np.array(input_grid)
    seq_len = len(input_seq)

    # initialize output_grid with zeros, same size as input
    output_grid = np.zeros_like(input_seq)

    # Find the properties of the non-zero block in the input sequence
    start_index, block_length, block_value = find_block_properties(input_seq)

    # If no valid block was found (e.g., all zeros or invalid format)
    if start_index == -1:
        return output_grid # Return the grid of zeros

    # Calculate the new starting position for the block
    # Shift distance is equal to the block length
    new_start_index = start_index + block_length

    # Place the shifted block into the output grid
    # Iterate 'block_length' times to place each element
    for i in range(block_length):
        # Calculate the index in the output grid for the current element
        target_index = new_start_index + i

        # Check if the target index is within the bounds of the grid
        if 0 <= target_index < seq_len:
            # Place the block's value at the target index
            output_grid[target_index] = block_value
        # Else: The element is shifted off the end of the grid and is discarded
        # (the output_grid position remains 0).

    return output_grid