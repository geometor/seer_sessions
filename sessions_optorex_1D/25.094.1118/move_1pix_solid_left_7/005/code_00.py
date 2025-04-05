"""
Transforms a 1D NumPy array by finding the first contiguous block of identical 
non-zero integers. If such a block exists and is preceded by a zero, 
the block is swapped with that preceding zero. If the block starts at 
index 0 or no non-zero block is found, the original array is returned.
"""

import numpy as np

def find_first_non_zero_block(arr: np.ndarray) -> tuple | None:
    """
    Finds the start and end indices of the first contiguous block of 
    identical non-zero integers in a 1D NumPy array that is preceded by a zero.

    Args:
        arr: A 1D NumPy array of integers.

    Returns:
        A tuple (start_index, end_index) if a suitable block is found.
        Returns None if no non-zero block is found, or if the first block 
        found starts at index 0 or is not preceded by a zero.
    """
    start_index = -1
    end_index = -1
    block_digit = None

    for i, digit in enumerate(arr):
        # Found a non-zero digit
        if digit != 0:
            # If this is the start of a potential block
            if start_index == -1:
                # Check if the block starts at the very beginning or not preceded by 0
                if i == 0 or arr[i - 1] != 0:
                    # If it starts at 0, it doesn't fit the swap pattern.
                    # If not preceded by 0, it doesn't fit the swap pattern.
                    # Continue searching in case there's another block later that *does* fit.
                    # We only care about the *first* block *that meets the criteria*.
                    continue 
                else: # Preceded by zero, potential block start
                     start_index = i
                     block_digit = digit
                     end_index = i # Initialize end index
            # If continuing an existing block (started in the 'else' above)
            elif digit == block_digit:
                end_index = i
            # If found a different non-zero digit, the first suitable block ended
            elif digit != block_digit and start_index != -1: 
                 break # Stop after the first suitable block is fully identified
        # Found a zero
        elif digit == 0:
            # If we were tracking a suitable block, it just ended
            if start_index != -1:
                break # Stop after the first suitable block is fully identified

    # After loop, check if a valid block was found (start_index must have been set)
    if start_index != -1:
        return start_index, end_index
    else:
        # No block preceded by zero was found
        return None


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the block-shifting transformation to the input NumPy array.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A new 1D NumPy array with the transformation applied, or a copy of the 
        original array if no transformation is applicable.
    """
    
    # Locate the contiguous block of identical non-zero integers preceded by zero.
    block_indices = find_first_non_zero_block(input_grid)

    # If no such block exists return the original sequence unchanged.
    if block_indices is None:
        return input_grid.copy() 

    start_index, end_index = block_indices
    
    # Identify the index of the element immediately before the block.
    preceding_zero_index = start_index - 1

    # Create a copy to avoid modifying the original input array in place
    output_grid = input_grid.copy()

    # Extract the non-zero block
    non_zero_block = output_grid[start_index : end_index + 1]
    
    # Extract the preceding zero element (as an array slice)
    preceding_zero = output_grid[preceding_zero_index : preceding_zero_index + 1] # Slice maintains array type

    # Perform the swap in the output grid:
    # Place the non-zero block starting at the preceding zero's original position
    output_grid[preceding_zero_index : preceding_zero_index + len(non_zero_block)] = non_zero_block
    
    # Place the preceding zero immediately after the shifted block
    output_grid[preceding_zero_index + len(non_zero_block) : preceding_zero_index + len(non_zero_block) + 1] = preceding_zero

    # The elements before the preceding_zero_index and after the end_index 
    # remain in their original places in the copied output_grid.

    # Return the newly constructed sequence.
    return output_grid