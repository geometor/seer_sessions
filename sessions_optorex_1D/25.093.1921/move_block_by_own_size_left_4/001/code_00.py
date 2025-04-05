import numpy as np # Although not strictly necessary for lists, using numpy can be helpful for array operations if needed later.

"""
Shift a contiguous block of identical non-zero numbers leftwards within a sequence of zeros. 
The amount of the shift is equal to the length of the block itself.
"""

def find_non_zero_block(sequence):
    """
    Finds the first contiguous block of identical non-zero numbers in a sequence.

    Args:
        sequence: A list or numpy array of numbers.

    Returns:
        A tuple (value, start_index, length) if a block is found,
        otherwise None.
        - value: The non-zero value of the block elements.
        - start_index: The index where the block begins.
        - length: The number of elements in the block.
    """
    start_index = -1
    block_value = 0
    length = 0
    in_block = False

    for i, val in enumerate(sequence):
        if not in_block and val != 0:
            # Start of a potential block
            in_block = True
            start_index = i
            block_value = val
            length = 1
        elif in_block:
            if val == block_value:
                # Continue the block
                length += 1
            else:
                # End of the block (hit a different value or zero)
                break # Assuming only one block per sequence based on examples
    
    if start_index != -1:
        return block_value, start_index, length
    else:
        # No non-zero block found
        return None

def transform(input_sequence):
    """
    Transforms the input sequence by shifting the non-zero block leftwards.

    Args:
        input_sequence: A list of integers representing the input state.

    Returns:
        A list of integers representing the output state after the shift.
    """
    # Convert to list if it's not already, for easier manipulation
    input_list = list(input_sequence)
    n = len(input_list)

    # Initialize the output sequence with all zeros
    output_sequence = [0] * n

    # 1. Find the contiguous block of non-zero numbers
    block_info = find_non_zero_block(input_list)

    # Proceed only if a block was found
    if block_info:
        block_value, start_index, block_length = block_info

        # 2. Calculate the shift distance (equal to block length)
        shift_distance = block_length

        # 3. Calculate the new starting index
        # Ensure the new index doesn't go below 0, although based on examples
        # where start_index >= length, this shouldn't happen.
        new_start_index = max(0, start_index - shift_distance)

        # 4. Place the block into the output sequence at the new position
        for i in range(block_length):
            # Check bounds to prevent index errors, though the logic should keep it within bounds
            if new_start_index + i < n:
                output_sequence[new_start_index + i] = block_value

    # 5. Return the modified output sequence
    return output_sequence