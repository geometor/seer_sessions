"""
Transforms an input sequence (potentially a NumPy array) containing a single 
contiguous block of identical non-zero integers surrounded by zeros. The 
transformation shifts this block to the right by a distance equal to its length. 
Positions originally occupied by the block become zeros, and elements shifted 
beyond the sequence boundary are discarded.
"""

import numpy as np

def find_block(input_seq):
    """
    Finds the contiguous block of identical non-zero integers in the sequence.

    Args:
        input_seq: A NumPy array of integers.

    Returns:
        A tuple (start_index, block_length, block_value) if a block is found,
        otherwise None. Returns (-1, 0, 0) if no non-zero block found.
    """
    # Find indices of all non-zero elements
    non_zero_indices = np.where(input_seq != 0)[0]

    # If no non-zero elements, no block exists
    if len(non_zero_indices) == 0:
        return -1, 0, 0

    # Identify potential start, end, length, and value
    start_index = non_zero_indices[0]
    end_index = non_zero_indices[-1]
    block_length = len(non_zero_indices)
    block_value = input_seq[start_index]

    # Verify the block is contiguous (indices are sequential)
    # and all values within the identified range are identical to the first non-zero value.
    # Check 1: Indices must form a continuous range (e.g., [2, 3, 4], not [2, 4])
    is_contiguous = (end_index - start_index + 1) == block_length
    # Check 2: All elements within this range [start_index:end_index+1] must equal block_value
    # This also implicitly checks if the original non_zero_indices were indeed identical.
    is_uniform_in_range = np.all(input_seq[start_index : end_index + 1] == block_value)

    if is_contiguous and is_uniform_in_range:
        return start_index, block_length, block_value
    else:
        # This case should not happen based on problem description, but handles unexpected input
        # For robustness, perhaps return the first found block segment or raise error.
        # Following the initial assumption of a single block:
        print(f"Warning: Input {input_seq} does not contain a single contiguous block of identical non-zero numbers.")
        # Return the first detected non-zero element as a block of length 1 for fallback
        # Or return failure indicator:
        return -1, 0, 0 # Indicate failure / no valid block


def transform(input_grid):
    """
    Applies the block shifting transformation.

    Args:
        input_grid: A 1D NumPy array representing the input sequence.

    Returns:
        A 1D NumPy array representing the transformed sequence.
    """
    # Ensure input is a NumPy array
    input_seq = np.array(input_grid)
    seq_len = len(input_seq)

    # --- Step 1 & 2: Identify Block and Extract Properties ---
    start_index, block_length, block_value = find_block(input_seq)

    # --- Step 3: Handle No Block Found Case ---
    # If no valid block is found (or input is all zeros), return an array of zeros.
    if start_index == -1:
        return np.zeros_like(input_seq)

    # --- Step 1 (Initialization): Create Output Sequence ---
    # Initialize the output grid with zeros, same size as input
    output_grid = np.zeros_like(input_seq)

    # --- Step 4: Calculate New Position ---
    new_start_index = start_index + block_length

    # --- Step 5: Place Shifted Block ---
    # Iterate 'block_length' times to place each element of the block
    for i in range(block_length):
        # Calculate the target index in the output grid for the current element.
        target_index = new_start_index + i

        # Check if the target index is within the bounds of the output grid.
        if 0 <= target_index < seq_len:
            # Place the block's value at the valid target index.
            output_grid[target_index] = block_value
        # Else: Element is shifted off the end and implicitly discarded (output_grid remains 0)

    # --- Step 6: Return Output ---
    return output_grid