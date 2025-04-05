"""
Identifies a contiguous block of identical non-zero numbers within the input sequence.
Calculates the target starting index for the block in the output sequence by subtracting 3 from the block's starting index in the input sequence.
Creates a new output sequence of the same length as the input, initialized with zeros.
Places the identified block of non-zero numbers into the output sequence at the calculated target starting index.
Returns the resulting output sequence.
"""

import numpy as np # Using numpy for easier array manipulation, though standard lists would also work

def find_block(sequence):
    """
    Finds the first contiguous block of identical non-zero numbers.

    Args:
        sequence (list or np.array): The input sequence of numbers.

    Returns:
        tuple: (start_index, value, length) of the block, or (None, None, None) if no block found.
    """
    start_index = None
    value = None
    length = 0
    for i, current_value in enumerate(sequence):
        if current_value != 0:
            if start_index is None: # Start of a potential block
                start_index = i
                value = current_value
                length = 1
            elif current_value == value: # Continuing the current block
                length += 1
            else: # Found a different non-zero number, stop (assumes only one block)
                break
        elif start_index is not None: # End of the block detected (hit a zero)
            break
    if start_index is not None:
        return start_index, value, length
    else:
        return None, None, None

def transform(input_grid: str) -> str:
    """
    Transforms the input grid string by shifting the non-zero block 3 positions to the left.

    Args:
        input_grid: A string representing a sequence of space-separated integers.

    Returns:
        A string representing the transformed sequence of space-separated integers.
    """
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_grid.split()]
    n = len(input_list)

    # Initialize output_grid as a list of zeros with the same length
    output_list = [0] * n

    # Find the non-zero block in the input
    start_index, value, length = find_block(input_list)

    # If a block is found, place it in the output list shifted left by 3
    if start_index is not None:
        # Calculate the new starting index for the block
        new_start_index = start_index - 3

        # Place the block in the output list, ensuring indices are within bounds
        for i in range(length):
            output_index = new_start_index + i
            # Ensure we don't write outside the list boundaries
            if 0 <= output_index < n:
                output_list[output_index] = value

    # Format the output list back into a space-separated string
    output_grid = " ".join(map(str, output_list))

    return output_grid
