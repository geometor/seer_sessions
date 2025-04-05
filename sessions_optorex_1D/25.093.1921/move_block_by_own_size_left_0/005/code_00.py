import math
from typing import List, Tuple, Optional, Union
import numpy as np # Import numpy to handle potential array inputs

"""
Transforms an input sequence (list or 1D numpy array) of integers.
The transformation involves the following steps:
1. Identify a single contiguous block of identical, non-zero integers within the input sequence.
2. Determine the value (V), starting index (S_in), and length (L) of this block.
3. Calculate a shift amount equal to the block's length (shift = L).
4. Calculate the target starting index (S_out) for the block in the output sequence: S_out = S_in - shift.
5. Create an output sequence of the same length as the input, initialized with zeros.
6. Place the identified block (value V, length L) into the output sequence starting at index S_out. 
   Elements are placed only if their target index is within the valid bounds [0, N-1] of the sequence.
"""

def find_block(sequence: List[int]) -> Optional[Tuple[int, int, int]]:
    """
    Finds the first contiguous block of identical non-zero digits.

    Args:
        sequence: The input list of integers.

    Returns:
        A tuple containing (block_value, start_index, block_length),
        or None if no such block is found.
    """
    start_index = -1
    block_value = 0
    block_length = 0
    n = len(sequence)

    # Iterate through the sequence to find the start of a non-zero block
    for i in range(n):
        val = sequence[i]
        # Check if the element is non-zero to start or identify a block
        if val != 0:
            # This is the start of the block we are looking for
            start_index = i
            block_value = val
            block_length = 1
            # Continue from the next element to find the end of the block
            for j in range(i + 1, n):
                if sequence[j] == block_value:
                    block_length += 1
                else:
                    # End of block (different value or zero encountered)
                    break
            # Found the block and its length, we can stop searching
            break

    # Return block details if one was found
    if start_index != -1:
        return block_value, start_index, block_length
    else:
        # No non-zero block found in the sequence
        return None

def transform(input_grid: Union[List[int], np.ndarray]) -> List[int]:
    """
    Applies the block shifting transformation to the input sequence.

    Args:
        input_grid: The input sequence, potentially a list or a NumPy array.

    Returns:
        A new list representing the transformed sequence.
    """
    # Ensure input is a standard Python list to avoid potential numpy ambiguity errors
    # and work with standard list indexing.
    if isinstance(input_grid, np.ndarray):
        # If it's a numpy array, flatten it (if needed, though examples are 1D)
        # and convert to a list.
        input_list = input_grid.flatten().tolist()
    else:
        # Assume it's already list-like (list, tuple, etc.) and convert to list
        input_list = list(input_grid)

    n = len(input_list)

    # Initialize output_grid with zeros, same size as input
    output_grid = [0] * n

    # Find the non-zero block details (value, start index, length)
    block_info = find_block(input_list)

    # If a block was found, proceed with the transformation
    if block_info:
        block_value, start_index_input, block_length = block_info

        # Calculate the shift amount (equal to block length)
        shift_amount = block_length

        # Calculate the new starting index for the block in the output
        start_index_output = start_index_input - shift_amount

        # Place the block into the output grid at the calculated position
        # Iterate for the length of the block
        for i in range(block_length):
            # Calculate the target index in the output grid
            target_index = start_index_output + i

            # Ensure the target index is within the valid bounds [0, n-1] of the output grid
            if 0 <= target_index < n:
                # Place the block's value at the target index
                output_grid[target_index] = block_value
            # else: Elements shifted outside the grid bounds are implicitly handled
            # because output_grid is initialized with zeros.

    # Return the resulting transformed grid as a list
    return output_grid