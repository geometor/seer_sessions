"""
Transforms a NumPy array representing a sequence of integers. It finds the 
first contiguous block of identical non-zero integers that is immediately 
preceded by a zero. If found, this block is swapped with the preceding zero. 
If no such block exists (e.g., all zeros, the first block starts at index 0, 
or the first block is not preceded by a zero), the original array is returned.
Handles potentially multi-dimensional input by flattening it first.
"""

import numpy as np

def find_first_valid_non_zero_block(arr_1d: np.ndarray) -> tuple | None:
    """
    Finds the start and end indices of the first contiguous block of 
    identical non-zero integers in a 1D NumPy array that is preceded by a zero.

    Args:
        arr_1d: A 1D NumPy array of integers.

    Returns:
        A tuple (start_index, end_index) if a suitable block is found.
        Returns None if no such block is found.
    """
    start_index = -1
    end_index = -1
    block_digit = None

    # Iterate through the sequence, starting from index 1 to check the preceding element
    for i in range(1, len(arr_1d)):
        current_digit = arr_1d[i]
        previous_digit = arr_1d[i-1]

        # Check for the start condition: non-zero digit preceded by a zero
        if current_digit != 0 and previous_digit == 0:
            # Found the start of the first valid block
            start_index = i
            end_index = i
            block_digit = current_digit

            # Continue scanning to find the end of this block
            for j in range(i + 1, len(arr_1d)):
                if arr_1d[j] == block_digit:
                    end_index = j # Extend the block
                else:
                    break # Block ended
            
            # Once the first valid block is found and its end determined, stop searching
            break 

    # Return indices if a valid block was found
    if start_index != -1:
        return start_index, end_index
    else:
        # No block preceded by zero was found
        return None


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the block-shifting transformation to the input NumPy array.

    Args:
        input_grid: A NumPy array (potentially multi-dimensional) of integers.

    Returns:
        A new NumPy array (flattened to 1D) with the transformation applied, 
        or a copy of the flattened original array if no transformation is applicable.
    """
    
    # Flatten the input grid to ensure it's 1D for processing
    # Create a copy to avoid modifying the original input if no swap occurs
    sequence = input_grid.flatten().copy() 
    original_shape = input_grid.shape # Store original shape if needed later

    # Locate the first contiguous block of identical non-zero integers preceded by zero.
    block_indices = find_first_valid_non_zero_block(sequence)

    # If no such block exists, return the flattened sequence unchanged.
    if block_indices is None:
        # Decide on output shape: For now, returning flattened. 
        # Could potentially reshape back: return sequence.reshape(original_shape)
        return sequence 

    start_index, end_index = block_indices
    
    # Identify the index of the element immediately before the block (the preceding zero).
    preceding_zero_index = start_index - 1

    # Create a copy to perform the swap without altering the original sequence during the process
    output_sequence = sequence.copy()

    # Extract the non-zero block
    non_zero_block = sequence[start_index : end_index + 1]
    
    # Extract the preceding zero element value
    preceding_zero_value = sequence[preceding_zero_index] 

    # Perform the swap in the output sequence:
    # Place the non-zero block starting at the preceding zero's original position
    output_sequence[preceding_zero_index : preceding_zero_index + len(non_zero_block)] = non_zero_block
    
    # Place the preceding zero immediately after the shifted block
    # The index where the zero should go is: preceding_zero_index + length_of_block
    zero_new_index = preceding_zero_index + len(non_zero_block)
    output_sequence[zero_new_index] = preceding_zero_value

    # The elements before the preceding_zero_index and after the end_index 
    # remain in their original places due to using a copy initially.

    # Return the newly constructed sequence.
    # Decide on output shape: For now, returning flattened.
    # Could potentially reshape back: return output_sequence.reshape(original_shape)
    return output_sequence