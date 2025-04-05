import numpy as np
from typing import Tuple, Optional

"""
Transforms a grid of integers by first flattening it into a 1D sequence. 
It then identifies the last contiguous block of identical non-zero digits within this sequence. 
If this block starts after the first position (index > 0) and is immediately preceded by a zero, 
the block is shifted one position to the left (replacing the zero), and a zero is appended 
to the end of the sequence to maintain its original length. 
Otherwise, the flattened sequence remains unchanged. The function returns the resulting 1D sequence.
"""

def _find_last_contiguous_block(data_array: np.ndarray) -> Optional[Tuple[int, int, int]]:
    """
    Finds the start index, end index, and value of the last contiguous block
    of identical non-zero digits in the 1D array.

    Args:
        data_array: The 1D numpy array of integers to search within.

    Returns:
        A tuple (start_index, end_index, value) if a block is found,
        otherwise None.
    """
    last_block_start = -1
    last_block_end = -1
    last_block_value = -1
    n = len(data_array)
    i = 0
    while i < n:
        current_val = data_array[i]
        # Check if the current element is non-zero
        if current_val != 0:
            # Potential start of a block
            start_index = i
            # Find where this block of identical digits ends
            j = i + 1
            while j < n and data_array[j] == current_val:
                j += 1
            end_index = j - 1 # The index of the last element in the block

            # Update the record of the last block found as we iterate left-to-right
            last_block_start = start_index
            last_block_end = end_index
            last_block_value = current_val

            # Continue the search *after* this block
            i = j
        else:
            # Current element is zero, move to the next element
            i += 1

    # After checking the whole array, return the details of the last block found
    if last_block_start != -1:
        return last_block_start, last_block_end, last_block_value
    else:
        # No non-zero blocks were found
        return None


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule based on the last contiguous block of non-zero digits
    in the flattened version of the input grid.

    Args:
        input_grid: A numpy array of integers (potentially multi-dimensional).

    Returns:
        A 1D numpy array representing the potentially modified sequence.
    """
    # Flatten the input grid into a 1D array
    flattened_array = input_grid.flatten()
    n = len(flattened_array)

    # Find the start index, end index, and value of the last contiguous block
    block_info = _find_last_contiguous_block(flattened_array)

    # Initialize output_grid as a copy of the flattened input
    output_array = np.copy(flattened_array)

    # Check if a valid block was found
    if block_info:
        start_index, end_index, _ = block_info

        # Check the condition: block exists, starts after index 0, and is preceded by 0
        if start_index > 0 and flattened_array[start_index - 1] == 0:
            # Condition met: perform the shift

            # Extract elements before the preceding zero
            part1 = flattened_array[:start_index - 1]
            # Extract the block itself
            block = flattened_array[start_index : end_index + 1]
            # Extract elements after the block
            part3 = flattened_array[end_index + 1:]
            # Define the appended zero with the correct dtype
            appended_zero = np.array([0], dtype=flattened_array.dtype)

            # Concatenate parts to form the new array
            # Note: np.concatenate requires a tuple of arrays
            output_array = np.concatenate((part1, block, part3, appended_zero))
        # else: condition not met, output_array remains the original flattened_array

    # Return the resulting 1D array
    return output_array