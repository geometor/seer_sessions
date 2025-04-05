import numpy as np

"""
Identifies a contiguous block of identical non-zero integers within the input NumPy array.
Shifts this block to the right by a number of positions equal to its own length.
The output is a new NumPy array of the same size, containing the shifted block and zeros elsewhere.
"""

def find_non_zero_block(sequence_array: np.ndarray) -> tuple:
    """
    Finds the first contiguous block of identical non-zero integers in a NumPy array.

    Args:
        sequence_array: A 1D NumPy array of integers.

    Returns:
        A tuple containing (block_value, block_length, block_start_index),
        or (None, 0, -1) if no non-zero block is found.
    """
    block_value = None
    block_length = 0
    block_start_index = -1

    for i, digit in enumerate(sequence_array):
        if digit != 0:
            # Found the start of a potential block
            block_value = digit
            block_start_index = i
            block_length = 1
            # Look ahead to find the end of the block
            for j in range(i + 1, len(sequence_array)):
                if sequence_array[j] == block_value:
                    block_length += 1
                else:
                    break # End of the block found
            # Since we assume only one block, we can return immediately
            return block_value, block_length, block_start_index
            
    # No non-zero block found (should not happen based on examples)
    return None, 0, -1


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input NumPy array by shifting the non-zero block.

    Args:
        input_grid: A 1D NumPy array containing a single block of identical non-zero digits.

    Returns:
        A new 1D NumPy array with the block shifted right by its length.
    """
    # Ensure input is treated as a 1D array if it's not already
    # (though examples seem consistently 1D)
    input_sequence = input_grid.flatten() if input_grid.ndim > 1 else input_grid
    n = len(input_sequence)

    # Identify the non-zero block using the helper function
    block_value, block_length, block_start_index = find_non_zero_block(input_sequence)

    # Handle case where no block is found (return zeros or original based on spec)
    # Based on examples, a block always exists. If not found, maybe return zeros.
    if block_value is None:
        return np.zeros_like(input_sequence) 

    # Calculate the target starting index for the block in the output sequence.
    # The shift amount is equal to the block's length.
    shift_amount = block_length
    new_start_index = block_start_index + shift_amount

    # Create a new NumPy array of the same length, filled with zeros.
    output_grid = np.zeros(n, dtype=input_sequence.dtype) # Match input dtype

    # Calculate the end index for slicing (exclusive)
    new_end_index = new_start_index + block_length

    # Place the identified block into the new array using NumPy slicing.
    # Check bounds to prevent errors if the shift goes beyond the array length.
    if new_start_index < n:
        # Calculate the actual length to place, considering boundary
        actual_length = min(block_length, n - new_start_index)
        output_grid[new_start_index : new_start_index + actual_length] = block_value
        
    # Reshape the output to match the original input grid's shape if necessary
    # (though examples are 1D, this adds robustness if inputs could be 2D later)
    if input_grid.ndim > 1:
         output_grid = output_grid.reshape(input_grid.shape)

    return output_grid