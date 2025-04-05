import numpy as np

"""
Identifies a single contiguous block of identical non-zero integers within a 12-element input sequence (list or numpy array). 
Shifts this block 4 positions to the left, ensuring the starting index does not go below 0. 
Returns a new 12-element numpy array with the shifted block, padding the remaining positions with zeros.
"""

def _find_non_zero_block(data: np.ndarray) -> tuple[int | None, int, int]:
    """
    Finds the first contiguous block of identical non-zero integers.

    Args:
        data: The input sequence as a numpy array.

    Returns:
        A tuple containing:
        - The non-zero integer composing the block (or None if no block found).
        - The length (count) of the block.
        - The starting index of the block.
        Returns (None, 0, -1) if no non-zero block is found.
    """
    start_index = -1
    block_digit = None
    block_length = 0
    n = len(data)

    for i in range(n):
        # Ensure comparison with standard python int if data is numpy type
        current_digit = int(data[i])

        if current_digit != 0:
            # Found a non-zero digit
            if block_digit is None:
                # This is the start of the first block found
                block_digit = current_digit
                start_index = i
                block_length = 1
            elif current_digit == block_digit:
                # This digit continues the current block
                block_length += 1
            else:
                # Found a non-zero digit different from the current block
                # Since the assumption is only one block exists, we stop here.
                break
        elif block_digit is not None:
            # Found a zero after a block was started, indicating the end of the block
            break

    # After loop, return findings
    if block_digit is None:
        return None, 0, -1 # No non-zero block found

    return block_digit, block_length, start_index


def transform(input_grid) -> np.ndarray:
    """
    Applies the block shifting transformation to the input sequence.

    Args:
        input_grid: The input sequence (list or numpy array of 12 integers).

    Returns:
        A numpy array representing the transformed sequence.
    """
    # Ensure input is a numpy array and get its length
    input_sequence = np.array(input_grid, dtype=int)
    n = len(input_sequence)

    # Define expected length (could be parameterised if needed)
    expected_length = 12
    if n != expected_length:
        # Handle unexpected length - returning an empty or zero array might be safest
        # For this specific task, we assume length is always 12 based on examples.
        # Initialize output based on actual length found, but this deviates from spec.
        # Sticking to 12 based on examples:
        n = expected_length


    # Initialize output grid with zeros
    output_grid = np.zeros(n, dtype=int)

    # Find the non-zero block in the input sequence
    block_digit, block_length, start_index = _find_non_zero_block(input_sequence)

    # Proceed only if a valid block was found
    if block_digit is not None:
        # Calculate the target starting index for the block in the output grid
        # Shift left by 4 positions, clamping at index 0
        shift_amount = 4
        target_start_index = max(0, start_index - shift_amount)

        # Place the block into the output grid
        # Iterate for the length of the block
        for i in range(block_length):
            # Calculate the current index in the output grid
            current_output_index = target_start_index + i
            # Check if the index is within the bounds of the output grid
            if current_output_index < n:
                # Assign the block's digit to the position
                output_grid[current_output_index] = block_digit
            else:
                # Stop if the block exceeds the grid bounds
                break

    # Return the newly created output grid
    return output_grid