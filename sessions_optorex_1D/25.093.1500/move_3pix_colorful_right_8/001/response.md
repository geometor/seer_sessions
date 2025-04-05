```python
import numpy as np # Although not strictly necessary for this specific logic, it's good practice for grid/array tasks.
import re

"""
Identify a contiguous block of non-zero digits within a fixed-length (12) sequence.
Shift this block 3 positions to the right.
Fill the remaining positions in the output sequence with zeros.
"""

def find_nonzero_block(int_list):
    """
    Finds the start index, end index, and the values of the first contiguous block of non-zero digits.

    Args:
        int_list: A list of integers.

    Returns:
        A tuple (start_index, end_index, block_values) or (None, None, []) if no non-zero digits are found.
        start_index: The index of the first non-zero digit.
        end_index: The index of the last non-zero digit in the contiguous block starting at start_index.
        block_values: A list containing the non-zero digits in the block.
    """
    start_index = -1
    end_index = -1
    block_values = []

    # Find the first non-zero digit
    for i, val in enumerate(int_list):
        if val != 0:
            start_index = i
            break

    # If no non-zero digit found, return early
    if start_index == -1:
        return None, None, []

    # Find the end of the contiguous block and collect values
    for i in range(start_index, len(int_list)):
        if int_list[i] != 0:
            end_index = i
            block_values.append(int_list[i])
        else:
            # Stop as soon as a zero is encountered after the block started
            break

    return start_index, end_index, block_values


def transform(input_str):
    """
    Transforms the input sequence string by shifting the non-zero block.

    Args:
        input_str: A string containing space-separated digits (e.g., "0 0 1 2 3 0 0").

    Returns:
        A string containing the transformed sequence with space-separated digits.
    """
    # Parse the input string into a list of integers
    input_list = [int(d) for d in input_str.split()]
    n = len(input_list) # Should be 12 based on examples

    # Initialize output_list with zeros
    output_list = [0] * n

    # Find the non-zero block in the input
    start_index, end_index, block_values = find_nonzero_block(input_list)

    # If a block was found, shift it
    if start_index is not None:
        # Calculate the new starting position
        shift_amount = 3
        new_start_index = start_index + shift_amount

        # Place the block values into the output list at the new position
        # Ensure we don't write past the end of the list
        for i, value in enumerate(block_values):
            output_index = new_start_index + i
            if output_index < n: # Check bounds
                output_list[output_index] = value

    # Format the output list back into a space-separated string
    output_str = " ".join(map(str, output_list))

    return output_str

```