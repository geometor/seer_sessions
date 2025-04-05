"""
Transforms an input sequence of integers by identifying all contiguous blocks of non-zero
integers, selecting the longest block (with the earliest starting index used to break ties),
and creating an output sequence of the same length containing only the elements of that
selected block in their original positions, with all other elements set to zero. If the input
is empty or contains no non-zero numbers, the output is an empty list or a list of zeros,
respectively.
"""

import numpy as np
import math
import collections # Although not strictly needed for the final logic, kept for potential future use

def find_nonzero_blocks(sequence):
    """
    Identifies contiguous blocks of non-zero numbers in a sequence.

    Args:
        sequence: A list or 1D NumPy array of numbers.

    Returns:
        A list of dictionaries, where each dictionary represents a block
        and contains 'start', 'end', and 'length' keys.
        Returns an empty list if no non-zero blocks are found or input is empty.
    """
    blocks = []
    start_index = -1
    n = len(sequence)

    if n == 0:
        return []

    for i, num in enumerate(sequence):
        # Check if current number is non-zero
        if num != 0:
            # If we are not already in a block, mark the start
            if start_index == -1:
                start_index = i
        # Check if current number is zero or we are at the end of the list
        if (num == 0 or i == n - 1) and start_index != -1:
            # If it's the end of the list and the last element is non-zero, the block ends here
            end_index = i if num != 0 else i - 1
            # Record the block if it's valid (start <= end)
            if start_index <= end_index:
                 blocks.append({
                    'start': start_index,
                    'end': end_index,
                    'length': end_index - start_index + 1
                })
            # Reset the start index as the block has ended
            start_index = -1

    return blocks

def select_target_block(blocks):
    """
    Selects the longest block from a list of blocks.
    If there's a tie in length, selects the one with the smallest start index.

    Args:
        blocks: A list of block dictionaries (output from find_nonzero_blocks).

    Returns:
        The dictionary representing the selected block, or None if the input list is empty.
    """
    if not blocks:
        return None

    # Find the maximum length among all blocks
    max_length = 0
    for block in blocks:
        if block['length'] > max_length:
            max_length = block['length']

    # Filter blocks to keep only those with the maximum length
    longest_blocks = [block for block in blocks if block['length'] == max_length]

    # Among the longest blocks, find the one with the minimum start index
    # If only one longest block, it will be selected by default
    # min() function with a key naturally handles finding the minimum start index
    selected_block = min(longest_blocks, key=lambda b: b['start'])

    return selected_block


def transform(input_grid):
    """
    Applies the transformation rule to the input grid (sequence).

    Args:
        input_grid: A sequence of numbers, likely a NumPy array from the environment.

    Returns:
        A list of integers representing the transformed sequence.
    """
    # Ensure input is treated as a 1D sequence (flatten if necessary) and convert to list
    if isinstance(input_grid, np.ndarray):
        # Handle potentially empty numpy array after flatten
        input_list = input_grid.flatten().tolist()
    else:
        # Assume it's already list-like, ensure it's a list
        input_list = list(input_grid)

    # Handle empty input list explicitly
    if not input_list:
        return []

    # Initialize output_list with zeros, same length as input
    output_list = [0] * len(input_list)

    # Find all non-zero blocks in the input list
    blocks = find_nonzero_blocks(input_list)

    # Select the target block (longest, earliest start index for ties)
    selected_block = select_target_block(blocks)

    # If a block was selected, copy its elements from the input to the output
    if selected_block:
        start = selected_block['start']
        end = selected_block['end']
        # Slice the original input list and place it into the output list
        output_list[start : end + 1] = input_list[start : end + 1]

    # Return the transformed list
    return output_list