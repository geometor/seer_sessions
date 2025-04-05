"""
Transforms an input sequence of 12 integers by identifying a single contiguous block of identical non-zero integers and shifting this block exactly two positions to the right. The remaining positions are filled with zeros.
"""

import re # Using re for potentially finding the block, although simpler list operations might suffice

def _find_non_zero_block_indices(sequence):
    """
    Finds the start and end indices of the first contiguous non-zero block.
    Returns (start_index, end_index) or (None, None) if no non-zero block is found.
    """
    start_index = -1
    end_index = -1
    for i, val in enumerate(sequence):
        if val != 0:
            if start_index == -1:
                start_index = i
            end_index = i
        elif start_index != -1:
            # Found a zero after the block started, so the block ended at the previous index
            break
    if start_index == -1:
        return None, None # No non-zero elements found
    return start_index, end_index

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string.

    Args:
        input_str: A string of space-separated integers.

    Returns:
        A string of space-separated integers representing the transformed sequence.
    """
    # 1. Parse the input string into a list of integers
    input_sequence = [int(x) for x in input_str.split()]
    sequence_length = len(input_sequence)

    # 2. Initialize an output_sequence as a list of zeros with the same length
    output_sequence = [0] * sequence_length

    # 3. Find the starting and ending indices of the non-zero block
    start_index, end_index = _find_non_zero_block_indices(input_sequence)

    # 4. If a non-zero block exists, proceed with the shift
    if start_index is not None and end_index is not None:
        # 5. Extract the non-zero block
        non_zero_block = input_sequence[start_index : end_index + 1]

        # 6. Calculate the new starting index for the block
        new_start_index = start_index + 2

        # 7. Place the extracted non-zero block into the output_sequence at the new position
        # Iterate through the block and place elements, ensuring we don't go out of bounds
        for i, value in enumerate(non_zero_block):
            target_index = new_start_index + i
            if target_index < sequence_length: # Check boundary condition
                output_sequence[target_index] = value
            # If target_index >= sequence_length, the block element shifts off the end

    # 8. Convert the output_sequence back into a space-separated string
    output_str = " ".join(map(str, output_sequence))

    return output_str
