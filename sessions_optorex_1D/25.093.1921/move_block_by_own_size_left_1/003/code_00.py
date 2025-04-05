import numpy as np # NumPy can be useful for array operations, though standard lists suffice here.
from typing import List, Tuple, Optional, Union

"""
Shifts a contiguous block of non-zero numbers within a sequence (list or 1D NumPy array) 
to the left by an amount equal to the length of the block. Zeros fill the remaining space.
"""

def _find_non_zero_block(data: Union[List[int], np.ndarray]) -> Tuple[Optional[List[int]], int, int]:
    """
    Finds the first contiguous block of non-zero numbers in the sequence.

    Args:
        data: The input sequence (list or 1D NumPy array) of integers.

    Returns:
        A tuple containing:
        - The list of numbers in the block (or None if no block is found).
        - The starting index of the block (or -1 if not found).
        - The ending index of the block (or -1 if not found).
    """
    start_index = -1
    end_index = -1
    n = len(data)

    # Iterate to find the start of the block
    for i in range(n):
        if data[i] != 0:
            start_index = i
            break

    # If no non-zero element found, return None
    if start_index == -1:
        return None, -1, -1

    # Iterate from the start index to find the end of the block
    end_index = start_index
    for i in range(start_index + 1, n):
        if data[i] != 0:
            end_index = i
        else:
            # Found the first zero after the block started
            break
            
    # Extract the block
    block = list(data[start_index : end_index + 1]) # Ensure it's a list

    return block, start_index, end_index

def transform(input_grid: Union[List[int], np.ndarray]) -> Union[List[int], np.ndarray]:
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_grid: The input sequence (list or 1D NumPy array) of integers.

    Returns:
        The transformed sequence (list or 1D NumPy array, matching input type if possible) 
        with the non-zero block shifted left by its length.
    """
    # Determine input type and length
    is_numpy = isinstance(input_grid, np.ndarray)
    input_list = list(input_grid) if is_numpy else input_grid
    n = len(input_list)

    # 1. Locate the contiguous block of non-zero numbers.
    non_zero_block, start_index, end_index = _find_non_zero_block(input_list)

    # Handle case where no non-zero block is found (return original or zeros)
    if non_zero_block is None:
        # Returning zeros matches the implicit pattern of filling empty space
        output_list = [0] * n
        return np.array(output_list) if is_numpy else output_list


    # 2. Calculate the length of the non-zero block.
    block_length = len(non_zero_block) # or end_index - start_index + 1

    # 3. Calculate the shift amount (equal to block length).
    shift_amount = block_length

    # 4. Calculate the new start index, ensuring it's not negative.
    new_start_index = start_index - shift_amount
    new_start_index = max(0, new_start_index)

    # 5. Create an output list of the same size, initialized with zeros.
    output_list = [0] * n

    # 6. Place the non-zero block into the output list at the new start index.
    # Iterate through the block elements and place them correctly.
    for i in range(block_length):
        output_index = new_start_index + i
        # Ensure we don't write past the end of the list (shouldn't happen with left shift)
        # or before the beginning (handled by clamping new_start_index)
        if 0 <= output_index < n:
            output_list[output_index] = non_zero_block[i]
        # else: block shifted partially or fully off the left edge - ignore those elements

    # Return in the original type if possible
    return np.array(output_list) if is_numpy else output_list